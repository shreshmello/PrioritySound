def simulate_alert(sound, priority, timestamp):
    """
    Create a simulated alert dict for the dashboard feed.
    Args:
        sound (str): Name of the sound detected.
        priority (str): Priority level (emergency, high, medium, low).
        timestamp (str): Time of detection.
    Returns:
        dict: Alert information including color for UI (matches pastel theme).
    """
    colors = {
        "emergency": "#FFB3BA",  # pastel red
        "high": "#FFFFBA",       # pastel yellow
        "medium": "#BAFFC9",     # pastel green
        "low": "#D3D3D3"         # light gray
    }
    return {
        "sound": sound,
        "priority": priority,
        "color": colors.get(priority, "#D3D3D3"),
        "time": timestamp
    }
