def simulate_alert(sound, priority, timestamp):
    # Generate a colored badge and return a dict for live feed
    colors = {
        "emergency":"red",
        "high":"yellow",
        "medium":"orange",
        "low":"blue"
    }
    return {
        "sound":sound,
        "priority":priority,
        "color":colors.get(priority,"gray"),
        "time":timestamp
    }
