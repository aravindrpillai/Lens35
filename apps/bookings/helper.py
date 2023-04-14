from datetime import datetime
import json

def create_lifecycle_event(event_details, field=None, old_value=None, new_value=None):
    return {
        "time" : str(datetime.now()),
        "event" : event_details,
        "value_change": { "field":field, "old_value": str(old_value), "new_value": str(new_value) } if(field!=None) else None
    }

def append_with_previous_lifecycle(previous_json, new_json):
    if(previous_json == None or previous_json == [] or previous_json == ""):
        return json.dumps(new_json)
    else:
        try:
            previous_json = json.loads(previous_json)
        except:
            pass
        if(previous_json == None or previous_json == []):
            return json.dumps(new_json)
        new_json = previous_json + [new_json]
        return json.dumps(new_json)