# Utility Functions for PrioritySound
# Helper functions for alert generation and data processing

def simulate_alert(sound, priority, timestamp):
    """Create alert data structure for display in the UI"""
    colors = {
        "emergency": "red",
        "high": "yellow",
        "medium": "orange",
        "low": "blue"
    }
    return {
        "sound": sound,
        "priority": priority,
        "color": colors.get(priority, "gray"),
        "time": timestamp
    }
