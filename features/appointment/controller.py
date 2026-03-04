"""
Appointment Controller Module.
Orchestrates appointment rules, pricing, and role-based filtering.
"""
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.utils.date_utils import get_now_mx
from features.appointment.dao import AppointmentDAO
from features.service.dao import ServiceDAO
from features.user.dao import UserDAO
from features.vehicle.dao import VehicleDAO
from features.appointment.schemas import AppointmentCreate, AppointmentUpdate
from features.user.models import User
from common.utils.responses import ErrorMessages

class AppointmentController:
    def __init__(self, db: AsyncSession):
        self.appointment_dao = AppointmentDAO(db)
        self.service_dao = ServiceDAO(db)
        self.vehicle_dao = VehicleDAO(db)
        self.user_dao = UserDAO(db)

    async def schedule_appointment(self, appointment_in: AppointmentCreate, current_user: User):
        """
        Business Logic:
        1. Verify vehicle existence and ownership.
        2. Fetch official service price.
        3. Validate Roles for Cashier and Washer.
        """
        # --- 1. Ownership check ---
        vehicle = await self.vehicle_dao.get_by_id(appointment_in.vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found.")
        if current_user.role.name == "Customer" and vehicle.user_id != current_user.id:
            raise HTTPException(status_code=403, detail=ErrorMessages.FORBIDDEN_ROLE)

        # --- 2. Price Fetching ---
        service = await self.service_dao.get_by_id(appointment_in.service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found.")
        appointment_in.total_price = service.cost - appointment_in.discount

        # --- 3. VALIDACIÓN DE ROLES ---

        # Validar Cajero
        cashier = await self.user_dao.get_by_id(appointment_in.cashier_id)
        if not cashier or cashier.role.name not in ["Cashier", "Admin"]:
            raise HTTPException(
                status_code=400,
                detail=f"Error: El usuario con ID {appointment_in.cashier_id} no es un Cajero válido."
            )

        # Validar Lavador
        if appointment_in.washer_id:
            washer = await self.user_dao.get_by_id(appointment_in.washer_id)
            if not washer or washer.role.name != "Washer":
                raise HTTPException(
                    status_code=400,
                    detail=f"Error: El usuario con ID {appointment_in.washer_id} no es un Lavador."
                )

            # Bonus: Verificar si el lavador está ocupado
            # (Buscamos si tiene citas asignadas que estén "In Progress")
            washer_appointments = await self.appointment_dao.get_by_washer_id(washer.id)
            is_busy = any(appt.status == "In Progress" for appt in washer_appointments)
            if is_busy:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error: El lavador {washer.first_name} ya está lavando un auto en este momento."
                )
        return await self.appointment_dao.create(appointment_in)

    async def get_visible_appointments(self, current_user: User):
        """Filter data based on role (Customer sees theirs, Washer sees theirs, Admin sees all)."""
        if current_user.role.name == "Customer":
            return await self.appointment_dao.get_by_user_id(current_user.id)
        if current_user.role.name == "Washer":
            return await self.appointment_dao.get_by_washer_id(current_user.id)

        return await self.appointment_dao.get_all_with_details()

    async def update_appointment_status(self, appointment_id: int, new_status: str, current_user: User):
        """
        Updates appointment status and automatically sets timestamps.
        Rules:
        - 'In Progress' sets start_time.
        - 'Completed' sets end_time.
        """
        db_appointment = await self.appointment_dao.get_by_id(appointment_id)
        if not db_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")

        # Logic for automated timestamps
        update_data = {"status": new_status}
        if db_appointment.status in ["Cancelled", "Completed"]:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede cambiar el estado de una cita que ya está '{db_appointment.status}'."
            )
        if new_status == "In Progress":
            update_data["start_time"] = get_now_mx()
        elif new_status == "Completed":
            update_data["end_time"] = get_now_mx()

        return await self.appointment_dao.update_fields(db_appointment, update_data)

    async def get_daily_report(self, target_date: date):
        """
        Generates a flat, comprehensive report for a specific date.
        Calculates wash duration dynamically.
        """
        appointments = await self.appointment_dao.get_by_date(target_date)
        report = []

        for appt in appointments:
            # Format full names
            cashier_name = f"{appt.cashier.first_name} {appt.cashier.last_name} {appt.cashier.second_last_name}"
            washer_name = f"{appt.washer.first_name} {appt.washer.last_name} {appt.washer.second_last_name}" if appt.washer else "Sin asignar"

            # Calculate duration in minutes if both timestamps exist
            duration = None
            if appt.start_time and appt.end_time:
                time_diff = appt.end_time - appt.start_time
                duration = int(time_diff.total_seconds() // 60) # convert to  minutes

            report.append({
                "appointment_id": appt.id,
                "status": appt.status,
                "cashier_full_name": cashier_name,
                "washer_full_name": washer_name,
                "service_name": appt.service.name,
                "service_description": appt.service.description,
                "service_cost": appt.service.cost,
                "discount": appt.discount,
                "total_price": appt.total_price,
                "vehicle_plate": appt.vehicle.plate_number,
                "vehicle_brand": appt.vehicle.brand,
                "vehicle_model": appt.vehicle.model,
                "vehicle_color": appt.vehicle.color,
                "duration_minutes": duration
            })

        return report