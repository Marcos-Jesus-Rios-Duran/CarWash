"""_summary_
carwash_backend/features/vehicle/routes.py
_routes for vehicle feature_
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.config.database import get_db
from common.security.permissions import RoleChecker
from features.user.models import User
from features.vehicle.schemas import VehicleCreate, VehicleResponse, VehicleUpdate
from features.vehicle.controller import VehicleController

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Customer"]))
) -> VehicleResponse:
    """
    Register a new vehicle.
    - **Customers**: Can only register vehicles for themselves.
    - **Admins & Cashiers**: Can register vehicles for any valid user_id.
    """
    controller = VehicleController(db)
    return await controller.register_vehicle(vehicle, current_user)


@router.get("/", response_model=List[VehicleResponse])
async def list_vehicles(
    include_inactive: bool = Query(False, description="Include deactivated vehicles in the list"), # <--- El switch
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Customer"]))
) -> List[VehicleResponse]:
    """
    Retrieve a list of vehicles.
    """
    controller = VehicleController(db)
    # Importante: Le pasamos la variable al controlador y asegúrate que el controlador se la pase al DAO
    return await controller.get_allowed_vehicles(current_user, include_inactive)

@router.patch("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_in: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Customer"]))
) -> VehicleResponse:
    """
    Update details of an existing vehicle (e.g., color, doors).
    - **Customers**: Can only update their own vehicles.
    """
    controller = VehicleController(db)
    return await controller.update_vehicle(vehicle_id, vehicle_in, current_user)

@router.delete("/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Customer"]))
):
    """
    Delete a vehicle from the system.
    - **Customers**: Can only delete their own vehicles.
    """
    controller = VehicleController(db)
    return await controller.delete_vehicle(vehicle_id, current_user)

@router.get("/plate/{plate_number}", response_model=VehicleResponse)
async def get_vehicle_by_plate(
    plate_number: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Admin", "Cashier", "Customer"]))
):
    """
    Search for a specific vehicle by its plate number.
    - **Customers**: Can only find it if they own it.
    - **Admins & Cashiers**: Can find any vehicle.
    """
    # Necesitas agregar este pequeño método a tu VehicleController:
    controller = VehicleController(db)
    vehicle = await controller.vehicle_dao.get_by_plate(plate_number) # Asume que crearás get_by_plate en el DAO

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado.")

    # Regla de seguridad inteligente
    if current_user.role.name == "Customer" and vehicle.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este vehículo.")

    return vehicle