# ==========================================================
# EXPLANATION ENGINE
# ==========================================================

class ExplanationEngine:

    def generate_explanation(self, machine: dict) -> dict:
        """
        Generates simple AI explanation.
        Always returns safe structure.
        """

        machine_id = machine.get("machine_id", "unknown")

        anomaly = machine.get("anomaly_score", 0)
        temp = machine.get("temperature", 0)

        if anomaly > 0.65:
            risk = "High risk detected due to abnormal behavior."
        elif anomaly > 0.3:
            risk = "Moderate anomaly observed."
        else:
            risk = "Machine operating normally."

        return {
            "machine_id": machine_id,
            "summary": risk,
            "temperature": temp,
        }


# ✅ singleton
explanation_engine = ExplanationEngine()