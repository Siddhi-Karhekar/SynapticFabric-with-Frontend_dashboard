import random
from backend_fastapi.ai_engine.root_cause import analyze_root_cause

# ✅ ML MODEL
from ml_models.failure_model import predict_failure

# ✅ NEW
from ml_models.explainer import explain_prediction
from ml_models.anomaly_model import detect_anomaly


class MachineAnalyzer:

    def analyze_machines(self, machines):

        analyzed = []

        for machine in machines:

            temperature = machine.get("temperature", 0)
            torque = machine.get("torque", 0)
            tool_wear = machine.get("tool_wear", 0)
            vibration = machine.get("vibration_index", 0)

            # =====================================
            # 🧠 ANOMALY SCORE (PHYSICS BASE)
            # =====================================

            anomaly_score = (
                ((temperature - 290) / 50) * 0.25 +
                tool_wear * 0.35 +
                vibration * 0.30 +
                (torque / 100) * 0.10
            )

            anomaly_score = max(0, min(anomaly_score, 1))
            anomaly_score = round(anomaly_score, 3)

            machine["anomaly_score"] = anomaly_score

            # =====================================
            # 🔍 ROOT CAUSE
            # =====================================

            try:
                root_causes = analyze_root_cause(machine)
            except Exception as e:
                print("❌ ROOT CAUSE ERROR:", e)
                root_causes = []

            machine["root_cause"] = root_causes

            # BOOST
            for cause in root_causes:
                anomaly_score += 0.2 * cause.get("confidence", 0)

            anomaly_score = min(anomaly_score, 1)
            anomaly_score = round(anomaly_score, 3)
            machine["anomaly_score"] = anomaly_score

            # =====================================
            # 🔮 FAILURE PROBABILITY (ML FIRST)
            # =====================================

            try:
                failure_probability = predict_failure(machine)

                print(
                    f"[ML OK] {machine['machine_id']} | "
                    f"Anomaly={anomaly_score} | ML={failure_probability}"
                )

            except Exception as e:
                print("[ML FAILED]", e)

                failure_probability = anomaly_score * random.uniform(0.95, 1.05)
                failure_probability = min(failure_probability, 1)

            failure_probability = round(failure_probability, 3)

            machine["failure_probability"] = failure_probability
            machine["prediction"] = failure_probability  # 🔥 CRITICAL FIX

            # =====================================
            # 🧠 SHAP EXPLANATION
            # =====================================

            try:
                shap_values = explain_prediction(machine)
                machine["shap"] = shap_values

                main_factor = max(shap_values, key=lambda k: abs(shap_values[k]))
                machine["ai_reason"] = f"Primary factor: {main_factor}"

            except Exception as e:
                print("❌ SHAP ERROR:", e)
                machine["shap"] = {}
                machine["ai_reason"] = "Explanation unavailable"

            # =====================================
            # 🤖 ANOMALY MODEL
            # =====================================

            try:
                machine["anomaly_ml_score"] = detect_anomaly(machine)
            except Exception as e:
                print("❌ ANOMALY MODEL ERROR:", e)
                machine["anomaly_ml_score"] = 0

            # =====================================
            # ⏳ ADVANCED RUL
            # =====================================

            try:
                degradation_rate = (
                    tool_wear * 0.6 +
                    vibration * 0.3 +
                    (temperature - 290) / 100 * 0.1
                )

                degradation_rate = max(0.01, degradation_rate)

                rul_cycles = int((1 - failure_probability) / degradation_rate * 100)
                rul_cycles = max(10, min(rul_cycles, 300))

                rul_hours = round(rul_cycles / 50, 2)

                machine["rul_cycles"] = rul_cycles
                machine["rul_time"] = f"{rul_hours} hrs"

            except Exception as e:
                print("❌ RUL ERROR:", e)
                machine["rul_cycles"] = 0
                machine["rul_time"] = "unknown"

            # =====================================
            # 🚨 ALERTS
            # =====================================

            alerts = []

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

            for cause in root_causes:
                if cause.get("confidence", 0) > 0.5:
                    alerts.append({
                        "level": "CRITICAL" if cause["confidence"] > 0.75 else "WARNING",
                        "message": cause["issue"]
                    })

            machine["alerts"] = alerts

            # =====================================
            # 🟢 HEALTH
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

            if "prediction" not in machine:
                machine["prediction"] = anomaly_score

            analyzed.append(machine)

        return analyzed


machine_analyzer = MachineAnalyzer()