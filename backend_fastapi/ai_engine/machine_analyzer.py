# ==========================================================
# MACHINE INTELLIGENCE ENGINE (STABLE)
# ==========================================================

from datetime import datetime
from typing import List, Dict

from backend_fastapi.ai_engine.explanation_engine import explanation_engine
from backend_fastapi.ai_engine.context_store import LATEST_PLANT_CONTEXT


class MachineAnalyzer:

    # ---------------------------------
    # HEALTH STATUS
    # ---------------------------------
    def compute_health_status(self, machine: Dict) -> str:
        anomaly = machine.get("anomaly_score", 0)

        if anomaly < 0.3:
            return "healthy"
        elif anomaly < 0.65:
            return "warning"
        return "critical"

    # ---------------------------------
    # ALERTS
    # ---------------------------------
    def detect_alerts(self, machine: Dict):

        alerts = []
        machine_id = machine.get("machine_id", "unknown")

        if machine.get("temperature", 0) > 305:
            alerts.append({
                "level": "HIGH",
                "message": f"{machine_id} overheating"
            })

        if machine.get("vibration_index", 0) > 0.9:
            alerts.append({
                "level": "WARNING",
                "message": f"{machine_id} vibration increasing"
            })

        return alerts

    # ---------------------------------
    # PREDICTIVE MAINTENANCE
    # ---------------------------------
    def estimate_rul(self, machine: Dict):

        wear = machine.get("tool_wear", 0)
        vibration = machine.get("vibration_index", 0)
        temperature = machine.get("temperature", 0)

        wear_factor = wear
        vibration_factor = max(0, (vibration - 0.5) / 1.0)
        temp_factor = max(0, (temperature - 300) / 30)

        risk_score = (
            wear_factor * 0.5 +
            vibration_factor * 0.3 +
            temp_factor * 0.2
        )

        risk_score = min(max(risk_score, 0), 1)

        rul_hours = int((1 - risk_score) * 200)

        failure_probability = round(risk_score * 100, 1)

        return {
            "rul_hours": rul_hours,
            "failure_probability": failure_probability
        }

    # ---------------------------------
    # PLANT SUMMARY
    # ---------------------------------
    def generate_plant_summary(self, machines):

        total = len(machines)

        healthy = sum(m["health_status"] == "healthy" for m in machines)
        warning = sum(m["health_status"] == "warning" for m in machines)
        critical = sum(m["health_status"] == "critical" for m in machines)

        return (
            f"Plant Status: {healthy}/{total} healthy, "
            f"{warning} warning, {critical} critical."
        )

    # ---------------------------------
    # MAIN ANALYSIS PIPELINE
    # ---------------------------------
    def analyze_machines(self, machines: List[Dict]):

        analyzed = []
        all_alerts = []

        for machine in machines:

            if not isinstance(machine, dict):
                continue

            if "machine_id" not in machine:
                continue

            # health
            machine["health_status"] = self.compute_health_status(machine)

            # prediction
            machine["prediction"] = self.estimate_rul(machine)

            # alerts
            alerts = self.detect_alerts(machine)
            machine["alerts"] = alerts
            all_alerts.extend(alerts)

            # explanation
            machine["ai_explanation"] = \
                explanation_engine.generate_explanation(machine)

            analyzed.append(machine)

        summary = self.generate_plant_summary(analyzed)
        self.update_context_cache(analyzed, all_alerts, summary)

        return analyzed

    # ---------------------------------
    # CONTEXT MEMORY UPDATE
    # ---------------------------------
    def update_context_cache(self, machines, alerts, summary):

        LATEST_PLANT_CONTEXT["timestamp"] = \
            datetime.utcnow().isoformat()

        LATEST_PLANT_CONTEXT["machines"] = machines
        LATEST_PLANT_CONTEXT["alerts"] = alerts
        LATEST_PLANT_CONTEXT["plant_summary"] = summary

        LATEST_PLANT_CONTEXT["explanations"] = [
            m["ai_explanation"] for m in machines
        ]


machine_analyzer = MachineAnalyzer()