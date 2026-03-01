"""
Stats-focused DAO for business intelligence.
"""
from sqlalchemy import func, select
from features.appointment.models import Appointment

class AppointmentStatsDAO:
    def __init__(self, session):
        self.session = session

    async def get_daily_stats(self, target_date):
        """
        Calculates total revenue and counts by status for a specific day.
        """
        # Query for total revenue of completed appointments today
        revenue_query = select(func.sum(Appointment.total_price)).where(
            (func.date(Appointment.appointment_date) == target_date) &
            (Appointment.status == "Completed")
        )

        # Query for counts grouped by status
        counts_query = select(Appointment.status, func.count(Appointment.id)).where(
            func.date(Appointment.appointment_date) == target_date
        ).group_by(Appointment.status)

        revenue_res = await self.session.execute(revenue_query)
        counts_res = await self.session.execute(counts_query)

        return {
            "total_revenue": revenue_res.scalar() or 0.0,
            "status_breakdown": dict(counts_res.all())
        }
