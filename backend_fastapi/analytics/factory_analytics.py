from sqlalchemy.orm import Session
from sqlalchemy import func

from backend_fastapi.database.models import MachineLog


def compute_factory_analytics(db: Session):

    total_machines = db.query(MachineLog.machine_id).distinct().count()

    avg_failure = db.query(func.avg(MachineLog.failure_probability)).scalar()

    most_unstable = (
        db.query(
            MachineLog.machine_id,
            func.avg(MachineLog.vibration_index)
        )
        .group_by(MachineLog.machine_id)
        .order_by(func.avg(MachineLog.vibration_index).desc())
        .first()
    )

    plant_health = 1 - (avg_failure if avg_failure else 0)

    return {
        "plant_health_score": round(plant_health, 3),
        "avg_failure_probability": round(avg_failure or 0, 3),
        "most_unstable_machine": most_unstable.machine_id if most_unstable else None,
        "total_machines": total_machines
    }