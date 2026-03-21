from ml_models.failure_model import predict_failure

result = predict_failure({
    "temperature": 310,
    "torque": 55,
    "tool_wear": 0.8,
    "vibration_index": 0.9
})

print("Prediction:", result)