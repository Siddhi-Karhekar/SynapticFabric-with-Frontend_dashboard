from backend_fastapi.database.database import SessionLocal
from backend_fastapi.database.models import MachineLog


def log_machine_state(machine):

    db = SessionLocal()

    try:

        record = MachineLog(

            machine_id=machine["machine_id"],

            temperature=machine["temperature"],

            torque=machine["torque"],

            tool_wear=machine["tool_wear"],

            vibration_index=machine["vibration_index"],

            anomaly_score=machine["anomaly_score"],

            health_status=machine["health_status"],

            failure_probability = machine.get("failure_probability", 0)

        )

        db.add(record)

        db.commit()

    finally:

        db.close()