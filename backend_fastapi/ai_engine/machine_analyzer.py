import random
from backend_fastapi.ai_engine.root_cause import analyze_root_cause


class MachineAnalyzer:

    def __init__(self):
        pass

    def analyze_machines(self, machines):

        analyzed = []

        for machine in machines:

            # =====================================
            # SENSOR VALUES
            # =====================================

            temperature = machine.get("temperature", 0)
            torque = machine.get("torque", 0)
            tool_wear = machine.get("tool_wear", 0)
            vibration = machine.get("vibration_index", 0)

            # =====================================
            # ANOMALY SCORE
            # =====================================

            anomaly_score = (
                ((temperature - 290) / 30) * 0.3 +
                tool_wear * 0.35 +
                vibration * 0.25 +
                (torque / 100) * 0.1
            )

            anomaly_score = max(0, min(anomaly_score, 1))
            anomaly_score = round(anomaly_score, 3)

            machine["anomaly_score"] = anomaly_score

            # =====================================
            # FAILURE PROBABILITY
            # =====================================

            failure_probability = round(
                anomaly_score * random.uniform(0.8, 1.1),
                3
            )

            failure_probability = min(failure_probability, 1)

            machine["failure_probability"] = failure_probability

            # Frontend expects this
            machine["prediction"] = failure_probability

            # =====================================
            # HEALTH STATUS
            # =====================================

            if anomaly_score < 0.45:
                health_status = "Healthy"

            elif anomaly_score < 0.75:
                health_status = "Warning"

            else:
                health_status = "Critical"

            machine["health_status"] = health_status

            # =====================================
            # ALERTS
            # =====================================

            alerts = []

            # Temperature alerts
            if temperature > 300:
                alerts.append({
                    "level": "warning",
                    "message": "Temperature rising above normal"
                })

            if temperature > 304:
                alerts.append({
                    "level": "critical",
                    "message": "Machine overheating risk"
                })

            # Vibration alerts
            if vibration > 0.45:
                alerts.append({
                    "level": "warning",
                    "message": "Vibration levels increasing"
                })

            if vibration > 0.8:
                alerts.append({
                    "level": "critical",
                    "message": "Severe vibration detected"
                })

            # Tool wear alerts
            if tool_wear > 0.35:
                alerts.append({
                    "level": "warning",
                    "message": "Tool wear approaching limit"
                })

            if tool_wear > 0.7:
                alerts.append({
                    "level": "critical",
                    "message": "Tool wear near failure"
                })

            # AI health alerts
            if anomaly_score > 0.45:
                alerts.append({
                    "level": "warning",
                    "message": "Machine health degrading"
                })

            if anomaly_score > 0.75:
                alerts.append({
                    "level": "critical",
                    "message": "Machine failure risk high"
                })

            machine["alerts"] = alerts

            # =====================================
            # AI EXPLANATION
            # =====================================

            machine["ai_explanation"] = (
                f"Machine health classified as {health_status}. "
                f"Anomaly score {anomaly_score} with failure probability "
                f"{failure_probability}."
            )

            # =====================================
            # ROOT CAUSE ANALYSIS
            # =====================================

            machine["root_cause"] = analyze_root_cause(machine)

            analyzed.append(machine)

        return analyzed


machine_analyzer = MachineAnalyzer()