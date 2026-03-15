from sqlalchemy.orm import Session
from sqlalchemy import func

from backend_fastapi.database.models import MachineLog
from digital_twin.simulator import run_digital_twin
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer
from backend_fastapi.database.logger import log_machine_state


def compute_factory_analytics(db: Session):

    # Ensure at least one telemetry cycle runs
    machines = run_digital_twin()
    analyzed = machine_analyzer.analyze_machines(machines)

    for m in analyzed:
        log_machine_state(m)

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

    machines_needing_maintenance = (
        db.query(MachineLog.machine_id)
        .filter(MachineLog.failure_probability > 0.6)
        .distinct()
        .all()
    )

    plant_health = 1 - (avg_failure if avg_failure else 0)

    return {
        "plant_health_score": round(plant_health, 3),
        "avg_failure_probability": round(avg_failure or 0, 3),
        "most_unstable_machine": most_unstable.machine_id if most_unstable else None,
        "machines_needing_maintenance": [m[0] for m in machines_needing_maintenance],
        "total_machines": total_machines
    }