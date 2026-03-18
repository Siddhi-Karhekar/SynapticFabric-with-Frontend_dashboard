import random
from backend_fastapi.ai_engine.root_cause import analyze_root_cause


class MachineAnalyzer:

    def analyze_machines(self, machines):

        analyzed = []

        for machine in machines:

            temperature = machine.get("temperature", 0)
            torque = machine.get("torque", 0)
            tool_wear = machine.get("tool_wear", 0)
            vibration = machine.get("vibration_index", 0)

            # =====================================
            # 🧠 ANOMALY SCORE
            # =====================================

            anomaly_score = (
                ((temperature - 290) / 50) * 0.25 +
                tool_wear * 0.35 +
                vibration * 0.30 +
                (torque / 100) * 0.10
            )

            anomaly_score = max(0, min(anomaly_score, 1))

            # =====================================
            # 🔍 ROOT CAUSE
            # =====================================

            root_causes = analyze_root_cause(machine)
            machine["root_cause"] = root_causes

            # =====================================
            # BOOST FROM ROOT CAUSE
            # =====================================

            for cause in root_causes:
                confidence = cause.get("confidence", 0)
                anomaly_score += 0.2 * confidence

            anomaly_score = min(anomaly_score, 1)
            anomaly_score = round(anomaly_score, 3)

            machine["anomaly_score"] = anomaly_score

            # =====================================
            # 🔮 FAILURE PROBABILITY
            # =====================================

            failure_probability = anomaly_score * random.uniform(0.95, 1.05)
            failure_probability = min(failure_probability, 1)

            machine["failure_probability"] = round(failure_probability, 3)
            machine["prediction"] = machine["failure_probability"]

            # =====================================
            # 🚨 ALERTS (STRICT)
            # =====================================

            alerts = []

            # Only trigger alerts ABOVE SAFE ZONE

            if temperature > 300:
                alerts.append({"level": "WARNING", "message": "High temperature"})

            if temperature > 305:
                alerts.append({"level": "CRITICAL", "message": "Overheating risk"})

            if vibration > 0.6:
                alerts.append({"level": "WARNING", "message": "High vibration"})

            if vibration > 0.85:
                alerts.append({"level": "CRITICAL", "message": "Severe vibration"})

            if tool_wear > 0.6:
                alerts.append({"level": "WARNING", "message": "Tool wear high"})

            if tool_wear > 0.85:
                alerts.append({"level": "CRITICAL", "message": "Tool failure imminent"})

            # ✅ ADD ROOT CAUSE ONLY IF REAL ISSUE
            for cause in root_causes:
                if cause["confidence"] > 0.5:
                    alerts.append({
                        "level": "CRITICAL" if cause["confidence"] > 0.75 else "WARNING",
                        "message": cause["issue"]
                    })

            machine["alerts"] = alerts

            # =====================================
            # 🟢 HEALTH STATUS (STRICT)
            # =====================================

            if any(a["level"] == "CRITICAL" for a in alerts):
                health_status = "Critical"
            elif any(a["level"] == "WARNING" for a in alerts):
                health_status = "Warning"
            else:
                health_status = "Healthy"

            machine["health_status"] = health_status

            machine["ai_explanation"] = (
                f"{health_status} | anomaly={anomaly_score} | risk={failure_probability}"
            )

            analyzed.append(machine)

        return analyzed


machine_analyzer = MachineAnalyzer()