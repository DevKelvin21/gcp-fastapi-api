from datetime import datetime
from typing import Any

def make_serializable(obj: Any) -> Any:
    """
    Recursively convert Firestore data to a JSON-serializable format.
    - Converts Firestore's DatetimeWithNanoseconds to ISO-formatted strings.
    - Handles nested dictionaries and lists.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, 'to_dict'):  # Firestore DocumentSnapshot
        return make_serializable(obj.to_dict())
    elif hasattr(obj, 'items'):  # Dictionary
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    else:
        # For Firestore's DatetimeWithNanoseconds or other types
        try:
            return obj.isoformat()
        except AttributeError:
            # If the object doesn't have isoformat, return its string representation
            return str(obj)
