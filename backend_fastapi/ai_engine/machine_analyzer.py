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
            # 🧠 ANOMALY SCORE (SMOOTH + STABLE)
            # =====================================

            anomaly_score = (
                ((temperature - 290) / 50) * 0.25 +
                tool_wear * 0.4 +
                vibration * 0.25 +
                (torque / 100) * 0.1
            )

            anomaly_score = max(0, min(anomaly_score, 1))
            anomaly_score = round(anomaly_score, 3)

            machine["anomaly_score"] = anomaly_score

            # =====================================
            # 🔮 FAILURE PROBABILITY (STABLE)
            # =====================================

            failure_probability = round(
                anomaly_score * random.uniform(0.9, 1.05),
                3
            )

            failure_probability = min(failure_probability, 1)

            machine["failure_probability"] = failure_probability
            machine["prediction"] = failure_probability

            # =====================================
            # 🚨 ALERTS (PRIMARY DRIVER)
            # =====================================

            alerts = []

            # 🌡 TEMPERATURE
            if temperature > 300:
                alerts.append({
                    "level": "WARNING",
                    "message": "Temperature rising above normal"
                })

            if temperature > 305:
                alerts.append({
                    "level": "CRITICAL",
                    "message": "Machine overheating risk"
                })

            # 📉 VIBRATION
            if vibration > 0.6:
                alerts.append({
                    "level": "WARNING",
                    "message": "Vibration levels increasing"
                })

            if vibration > 0.85:
                alerts.append({
                    "level": "CRITICAL",
                    "message": "Severe vibration detected"
                })

            # 🛠 TOOL WEAR
            if tool_wear > 0.6:
                alerts.append({
                    "level": "WARNING",
                    "message": "Tool wear approaching limit"
                })

            if tool_wear > 0.85:
                alerts.append({
                    "level": "CRITICAL",
                    "message": "Tool failure imminent"
                })

            machine["alerts"] = alerts

            # =====================================
            # 🔥 HEALTH STATUS (ALERT-DRIVEN)
            # =====================================

            has_critical = any(a["level"] == "CRITICAL" for a in alerts)
            has_warning = any(a["level"] == "WARNING" for a in alerts)

            if has_critical:
                health_status = "Critical"
            elif has_warning:
                health_status = "Warning"
            else:
                health_status = "Healthy"

            machine["health_status"] = health_status

            # =====================================
            # 🤖 AI EXPLANATION
            # =====================================

            machine["ai_explanation"] = (
                f"Health: {health_status}. "
                f"Anomaly score {anomaly_score}, "
                f"Failure probability {failure_probability}."
            )

            # =====================================
            # 🔍 ROOT CAUSE (SYNCED WITH STATE)
            # =====================================

            machine["root_cause"] = analyze_root_cause(machine)

            analyzed.append(machine)

        return analyzed


# singleton
machine_analyzer = MachineAnalyzer()