from apps.bookings.helper import append_with_previous_lifecycle, create_lifecycle_event 
from apps.customers.models.customers import Customers
from util.regex import validate_and_format_pincode
from apps.bookings.models.bookings import Bookings
from apps.bookings.models.services import Services
from datetime import datetime, time, timedelta
from rest_framework.decorators import api_view
from util.google_maps import get_cordinates
from util.http import build_response
from lens35.constanst import EVENTS
from util.logger import logger
import traceback
import uuid

@api_view(['POST'])
def index(request):
    try:
        customer_id = request.headers.get("Identifier")
        customer = Customers.objects.get(customer_id = customer_id)
        data = request.data

        booking_id = data.get("booking_id",None)
        event = data.get("event",None)
        event_description = data.get("event_description",None)
        event_date = data.get("event_date",None)
        event_start_time = data.get("event_start_time",None)
        event_duration = data.get("event_duration",None)
        event_postal_code = data.get("event_postal_code",None)
        event_city = data.get("event_city",None)
        event_address = data.get("event_address",None)

        lifecycle = []
        reset_services_and_reevaluate_payment = False
        is_booking_update = True
      
        if(booking_id != None and booking_id != ""):
            booking = Bookings.objects.get(booking_id = booking_id)
        else:
            lifecycle.append(create_lifecycle_event("Booking Request Received"))
            is_booking_update = False
            booking = Bookings() 
            booking.booking_id = uuid.uuid4()
            booking.customer = customer

        #Event
        if(event != None and event != ""):
            allowed_events = [each_event[0] for each_event in EVENTS]
            event = event.lower()
            if(not event in allowed_events):
                raise Exception("Invalid Event. Value must be one amongst {}".format(str(allowed_events)))
            if(is_booking_update):
                if(booking.event != event):
                    lifecycle.append(create_lifecycle_event("Field modified", "event", booking.event, event))
                    reset_services_and_reevaluate_payment = True
            booking.event = event
        else:
            if(booking.event == None or booking.event == ""):
                raise Exception("Event cannot be empty")   
            
        #Event Description
        if(event_description != None and event_description != "" and event_description != booking.event_description):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_description", booking.event_description, event_description))
            booking.event_description = event_description
        else:
            if(booking.event_description == None or booking.event_description == ""):
                raise Exception("Please provide a short note about the booking")   

        
        #Event Date
        if(event_date != None and event_date != ""):
            event_date = datetime.fromisoformat(event_date).date() #YYYY_mm_dd
            if(event_date < datetime.now().date()):
                raise Exception("Event date must be on or after today")
            if(is_booking_update):
                if(str(booking.event_date) != str(event_date)):
                    lifecycle.append(create_lifecycle_event("Field modified", "event_date", booking.booking_date, event_date))
                    reset_services_and_reevaluate_payment = True
            booking.event_date = event_date
        else:
            if(booking.booking_date == None or booking.booking_date == ""):
                raise Exception("Event Date cannot be empty")   


        
        #Booking Start Time
        if(event_start_time != None and event_start_time != ""):
            event_start_time = time.fromisoformat(event_start_time) #HH:MM
            if(event_date == datetime.now().date() and ((datetime.now()+timedelta(minutes=59)).time() > event_start_time)):
                raise Exception("Booking must start atleast an hour from now")
            if(is_booking_update):
                if(str(booking.event_start_time) != str(event_start_time)):
                    lifecycle.append(create_lifecycle_event("Field modified", "event_start_time", booking.event_start_time, event_start_time))
                    reset_services_and_reevaluate_payment = True
            booking.event_start_time = event_start_time
        else:
            if(booking.event_start_time == None or booking.event_start_time == ""):
                raise Exception("Event Start Time cannot be empty")   


        #Booking Duration
        if(event_duration != None and event_duration != ""):
            if(event_duration < 1):
                raise Exception("Minimum Booking must be for 1 Hours")
            if(event_duration > 8):
                raise Exception("Booking cannot exceed 8 Hours")
            if(is_booking_update):
                if(booking.event_duration != event_duration):
                    lifecycle.append(create_lifecycle_event("Field modified", "event_duration", booking.event_duration, event_duration))
                    reset_services_and_reevaluate_payment = True
            booking.event_duration = event_duration
        else:
            if(booking.event_duration == None or booking.event_duration == ""):
                raise Exception("A minimum of 2 Hour booking is required")   

        #Booking Postal Code
        if(event_postal_code != None and event_postal_code != "" and event_postal_code != booking.event_postal_code):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_postal_code", booking.event_postal_code, event_postal_code))
                reset_services_and_reevaluate_payment = True
            booking.event_postal_code = validate_and_format_pincode(event_postal_code)
            address_updated = True
        else:
            if(booking.event_postal_code == None or booking.event_postal_code == ""):
                raise Exception("Event postal-code is mandatory")   

        address_updated = False
        #Booking City
        if(event_city != None and event_city != "" and event_city != booking.event_city):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_city", booking.event_city, event_city))
                reset_services_and_reevaluate_payment = True
            booking.event_city = event_city
            address_updated = True
        else:
            if(booking.event_city == None or booking.event_city == ""):
                raise Exception("Event city is mandatory")  
        
        #Booking Address
        if(event_address != None and event_address != "" and event_address != booking.event_address):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_address", booking.event_address, event_address))
                reset_services_and_reevaluate_payment = True
            booking.event_address = event_address            
        else:
            if(booking.event_address == None or booking.event_address == ""):
                raise Exception("Event Address is mandatory")  

        #Geocoding
        if(address_updated):
            if(booking.event_city == None or booking.event_city == "" or booking.event_postal_code == None  or booking.event_postal_code == ""):
                raise Exception("Event City and Postal code are mandatory - Required for geocoding")
            address = "{}, {}".format(booking.event_city, booking.event_postal_code)
            cord = get_cordinates(address)
            booking.event_latitude = cord[0]
            booking.event_longitude = cord[1]

        #Resetting Services
        if(reset_services_and_reevaluate_payment):
            has_service_updates = False
            for service in Services.objects.filter(booking = booking).exclude(employee = None, retired = True):
                service_lc = create_lifecycle_event("Removed assignment due to booking change", "employee", service.employee.employee_id, None)
                service.employee = None
                service.lifecycle = append_with_previous_lifecycle(service.lifecycle, service_lc) 
                service.save()
                has_service_updates = True
            if(has_service_updates):
                lifecycle.append(create_lifecycle_event("Removed service assignments", None))
        
        if(lifecycle != []):
            booking.lifecycle = append_with_previous_lifecycle(booking.lifecycle,lifecycle)

        booking.save()

        updated_fields = {
            "booking_id" : booking.booking_id,
            "event" : booking.event,
            "event_description" : booking.event_description,
            "event_date" : booking.event_date,
            "event_start_time" : booking.event_start_time,
            "event_duration" : booking.event_duration,
            "event_postal_code" : booking.event_postal_code,
            "event_city" : booking.event_city,
            "event_address" : booking.event_address,
        }
        return build_response(202, "Success", updated_fields)
    except Exception as e_0:
        logger.error('Failed to handle the booking request {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))