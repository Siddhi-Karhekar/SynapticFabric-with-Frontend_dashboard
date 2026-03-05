# ==========================================================
# EXPLANATION ENGINE — ROOT CAUSE + RECOMMENDATIONS
# ==========================================================

class ExplanationEngine:

    def generate_explanation(self, machine):

        vibration = machine.get("vibration_index", 0)
        wear = machine.get("tool_wear", 0)
        temp = machine.get("temperature", 0)

        causes = []
        actions = []

        # -----------------------------
        # Root Cause Analysis
        # -----------------------------
        if vibration > 1:
            causes.append("High vibration detected")
            actions.append("Inspect spindle alignment")

        if wear > 0.6:
            causes.append("Tool wear approaching failure threshold")
            actions.append("Replace cutting tool")

        if temp > 310:
            causes.append("Thermal stress detected")
            actions.append("Check cooling system")

        # Default state
        if not causes:
            causes.append("Machine operating within normal parameters")
            actions.append("No action required")

        return {
            "machine_id": machine.get("machine_id"),
            "causes": causes,
            "actions": actions
        }


# singleton instance
explanation_engine = ExplanationEngine()