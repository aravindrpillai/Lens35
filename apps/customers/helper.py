from lens35.constanst import PHOTOGRAPHER_RATE_PER_HOUR, VIDEOGRAPHER_RATE_PER_HOUR, DRONE_RATE_PER_HOUR
from apps.bookings.models.service_invoice_items import ServiceInvoiceItems
from lens35.constanst import CANCELLATION_CHARGE
from django.db.models import Q
from datetime import datetime
import json
import uuid


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
    

def create_service_invoice_item(service, cost_category):
    initial_service_cost = 0
    duration = service.booking.event_duration
    def get_description():
        if cost_category == "booking_cost":
            match service.service:
                case "photography" : return "Photographer (Rs.{} x {}Hrs)".format(PHOTOGRAPHER_RATE_PER_HOUR,duration) 
                case "videography" : return "Videographer (Rs.{} x {}Hrs)".format(VIDEOGRAPHER_RATE_PER_HOUR,duration) 
                case "drone_photography" : return "Drone Photographer (Rs.{} x {}Hrs)".format(DRONE_RATE_PER_HOUR,duration) 
                case "photo_editing" : return "Photo Editor (Rs.{} x {}Hrs)".format(0,duration)  
                case "video_editing" : return "Video Editor (Rs.{} x {}Hrs)".format(0,duration)  
                case __ : raise Exception("Failed to rate the service. invalid service code")
        if cost_category == "cancellation":
            match service.service:
                case "photography" : return "Photographer Cancellation Charge (Rs.{})".format(CANCELLATION_CHARGE)
                case "videography" : return "Photographer Cancellation Charge (Rs.{})".format(CANCELLATION_CHARGE)
                case "drone_photography" : return "Drone Photographer Cancellation Charge (Rs.{})".format(CANCELLATION_CHARGE)
                case "photo_editing" : return "PhotoEditor Cancellation Charge (Rs.{})".format(CANCELLATION_CHARGE)
                case "video_editing" : return "VideoEditor Cancellation Charge (Rs.{})".format(CANCELLATION_CHARGE)
                case __ : raise Exception("Failed to rate the service. invalid service code")
            
        return "TODO ::: ..COST CATEGORY NOT DEFINED.. "

    match service.service:
        case "photography" : initial_service_cost = PHOTOGRAPHER_RATE_PER_HOUR * duration
        case "videography" : initial_service_cost = VIDEOGRAPHER_RATE_PER_HOUR * duration
        case "drone_photography" : initial_service_cost = DRONE_RATE_PER_HOUR * duration
        case "photo_editing" : initial_service_cost = 0
        case "video_editing" : initial_service_cost = 0
        case __ : raise Exception("Failed to rate the service. invalid service code")

    if cost_category == "cancellation":
        bcs = ServiceInvoiceItems.objects.filter(service=service).filter(Q(cost_category = "booking_cost") | Q(cost_category = "discount"))
        for bc in bcs:
            bc.cost = 0#
            bc.description = bc.description.split("(")[0]+" (cancelled)"
            bc.save()

    service_invoice_item = ServiceInvoiceItems()
    service_invoice_item.invoice_item_id = uuid.uuid4()
    service_invoice_item.service = service
    service_invoice_item.cost = CANCELLATION_CHARGE if cost_category == "cancellation" else initial_service_cost
    service_invoice_item.cost_category = cost_category
    service_invoice_item.description = get_description()
    service_invoice_item.save()


# def __handle_charges(service, booking, is_delete):
#     if(is_delete and service.employee == None):
#         #cancellation charge is added only for assigned services.
#         return
    
#     charge = 0
#     match service.service:
#         case "photography"  : charge = PHOTOGRAPHER_RATE_PER_HOUR * booking.event_duration
#         case "videography"  : charge = VIDEOGRAPHER_RATE_PER_HOUR * booking.event_duration
#         case "drone"        : charge = DRONE_RATE_PER_HOUR * booking.event_duration
#         case __ : raise Exception("Failed to rate the service. invalid service code")

#     service_invoice_item = ServiceInvoiceItems()
#     service_invoice_item.invoice_item_id = uuid.uuid4()
#     service_invoice_item.service = service
#     service_invoice_item.cost = CANCELLATION_CHARGE if is_delete else charge
#     service_invoice_item.cost_category = "cancellation_charge" if is_delete else "booking_cost"
#     if(is_delete):
#          desc = "Cancellation charge for service {}. (Rs.{})".format(service.service.capitalize(), CANCELLATION_CHARGE)
#     else:
#         desc = "New Service charge for {}. ({}Hrs x Rs.{} = {})".format(service.service.capitalize(), booking.event_duration, PHOTOGRAPHER_RATE_PER_HOUR, charge)
#     service_invoice_item.description = desc
#     service_invoice_item.save()