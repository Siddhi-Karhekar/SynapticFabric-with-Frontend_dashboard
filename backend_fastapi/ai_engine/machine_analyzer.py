import random
from backend_fastapi.ai_engine.root_cause import analyze_root_cause


class MachineAnalyzer:

    def __init__(self):
        pass

    def analyze_machines(self, machines):

        analyzed = []

        for machine in machines:

            # =====================================
            # EXTRACT SENSOR VALUES
            # =====================================

            temperature = machine.get("temperature", 0)
            torque = machine.get("torque", 0)
            tool_wear = machine.get("tool_wear", 0)
            vibration = machine.get("vibration_index", 0)

            # =====================================
            # ANOMALY SCORE
            # =====================================

            anomaly_score = (
                (temperature / 120) * 0.3 +
                (torque / 120) * 0.25 +
                (tool_wear / 100) * 0.25 +
                vibration * 0.2
            )

            anomaly_score = round(min(anomaly_score, 1), 3)

            machine["anomaly_score"] = anomaly_score

            # =====================================
            # FAILURE PROBABILITY
            # =====================================

            failure_probability = round(
                anomaly_score * random.uniform(0.7, 1.1), 3
            )

            machine["failure_probability"] = min(failure_probability, 1)

            # 🔧 FIX FOR WEBSOCKET CRASH
            machine["prediction"] = machine["failure_probability"]

            # =====================================
            # HEALTH STATUS
            # =====================================

            if anomaly_score < 0.35:
                health_status = "Healthy"
            elif anomaly_score < 0.6:
                health_status = "Warning"
            else:
                health_status = "Critical"

            machine["health_status"] = health_status

            # =====================================
            # AI ALERTS
            # =====================================

            alerts = []

            if temperature > 85:
                alerts.append({
                    "level": "warning",
                    "message": "High temperature detected"
                })

            if vibration > 0.7:
                alerts.append({
                    "level": "warning",
                    "message": "High vibration levels"
                })

            if tool_wear > 80:
                alerts.append({
                    "level": "critical",
                    "message": "Tool wear extremely high"
                })

            if anomaly_score > 0.6:
                alerts.append({
                    "level": "critical",
                    "message": "Machine health critical"
                })

            machine["alerts"] = alerts

            # =====================================
            # AI EXPLANATION
            # =====================================

            machine["ai_explanation"] = (
                f"Machine health classified as {health_status}. "
                f"Anomaly score {anomaly_score} with failure probability "
                f"{machine['failure_probability']}."
            )

            # =====================================
            # ROOT CAUSE ANALYSIS
            # =====================================

            machine["root_cause"] = analyze_root_cause(machine)

            analyzed.append(machine)

        return analyzed


machine_analyzer = MachineAnalyzer()