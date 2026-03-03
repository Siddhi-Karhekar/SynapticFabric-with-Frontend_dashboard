def clean(data):
    if data["process_temperature_K"] > 400:
        return None
    return data