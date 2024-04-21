from apps.customers.helper import append_with_previous_lifecycle, create_lifecycle_event
from apps.customers.apis.bookings.fetch_services import fetch_services
from lens35.constanst import PHOTOGRAPHY, VIDEOGRAPHY, DRONE
from apps.customers.models.customers import Customers
from util.regex import validate_and_format_pincode
from apps.bookings.models.bookings import Bookings
from apps.bookings.models.services import Services
from datetime import datetime, time, timedelta
from rest_framework.decorators import api_view
from util.google_maps import get_cordinates
from util.http import build_response
from lens35.constanst import EVENTS
from django.db.models import Q
from util.logger import logger
import traceback
import uuid

#Note:
# This is the api which handles the whole booking
# Whatever data is been passed, that will be processed
# 1. If Booking ID is not passed, this request will be considered as a new booking and all available info will be saved and a new booking ID will be returned.
# 2. If booking ID is passed along with the data,then that request will be considered as an Update
# 3. Any kind of modification is possible untill "published flag is false" (published will be set to true once the payment is done)
# 4. Once the published flag is true, for furhter updates, the api looks for any services that are committed by the photographer.
#       a. If none of the services are commiiteed to a photographer, then the API simply save the update.
#           Note - Call InvoiceAPI once this is done to see any changes in charges.
#       b. If any of the service is committed - see action that happens for each field update
#          [event, event_description, event_date, event_start_time, event_duration, event_postal_code, event_city, event_address]
#          Set "Service.review" to true
#
#           [photography, videography, drone] 
#           any of this to false, set Service.retired to true 
#           if any of this is set to true (newly added service) - Create a new service as usual
#           Note- In both the above cases, charges will be taken care by InvoiceAPI.                        

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

        photographer = data.get("photography", False)
        videographer = data.get("videography", False)
        drone = data.get("drone", False)

        lifecycle = []
        is_booking_update = True
        booking_updated = False
        address_updated = False
        
        if(booking_id != None and booking_id != ""):
            booking = Bookings.objects.get(booking_id = booking_id)
            #TODO - Compare the current date and the booking event date - Update must be restricted when request comes after event date 
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
                    booking_updated = True
            booking.event = event
        else:
            if(booking.event == None or booking.event == ""):
                raise Exception("Event cannot be empty")   
            
        #Event Description
        if(event_description != None and event_description != "" and event_description != booking.event_description):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_description", booking.event_description, event_description))
                booking_updated = True
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
                    lifecycle.append(create_lifecycle_event("Field modified", "event_date", booking.event_date, event_date))
                    booking_updated = True
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
                    booking_updated = True
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
                    booking_updated = True
            booking.event_duration = event_duration
        else:
            if(booking.event_duration == None or booking.event_duration == ""):
                raise Exception("Booking duration is required")   

        #Booking Postal Code
        if(event_postal_code != None and event_postal_code != "" and event_postal_code != booking.event_postal_code):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_postal_code", booking.event_postal_code, event_postal_code))
                booking_updated = True
            booking.event_postal_code = validate_and_format_pincode(event_postal_code)
            address_updated = True
        else:
            if(booking.event_postal_code == None or booking.event_postal_code == ""):
                raise Exception("Event postal-code is mandatory")   

        #Booking City
        if(event_city != None and event_city != "" and event_city != booking.event_city):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_city", booking.event_city, event_city))
                booking_updated = True
            booking.event_city = event_city
            address_updated = True
        else:
            if(booking.event_city == None or booking.event_city == ""):
                raise Exception("Event city is mandatory")  
        
        #Booking Address
        if(event_address != None and event_address != "" and event_address != booking.event_address):
            if(is_booking_update):
                lifecycle.append(create_lifecycle_event("Field modified", "event_address", booking.event_address, event_address))
                booking_updated = True
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

        if(lifecycle != []):
            booking.lifecycle = append_with_previous_lifecycle(booking.lifecycle,lifecycle)


        booking.save()
        
        #handle Services
        services = Services.objects.filter(booking = booking).exclude(Q(retired = True) | Q(closed = True))
        __handle_each_service(booking, services, PHOTOGRAPHY, photographer, booking_updated)
        __handle_each_service(booking, services, VIDEOGRAPHY, videographer, booking_updated)
        __handle_each_service(booking, services, DRONE, drone, booking_updated)

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
            "services" : fetch_services(booking.booking_id, customer_id)
        }
        return build_response(202, "Success", updated_fields)
    except Exception as e_0:
        logger.error('Failed to handle the booking request {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))
    


def __handle_each_service(booking, services, service_name, add_this_service, has_booking_updated):
    this_services = services.filter(service = service_name)
    this_services_count = this_services.count()
    #no existing (this) service
    if(this_services_count == 0):
        if(add_this_service):
            #Request came to add new (this) service
            service = Services()
            service.service_id = uuid.uuid4()
            service.booking = booking
            service.service = service_name
            service.lifecycle = [create_lifecycle_event("Created new service: {}".format(service_name))]
            service.save()
            logger.info('Add {} service to booking : {}'.format(service_name, booking.booking_id))
    #Booking already has one or more this-sevice (it must be one only - handled belows)
    else:
        if(this_services_count > 1):
            # in case if there are more records, take the latest and delete others
            this_service = this_services.exclude(employee=None).latest('id')
            outdated_srvs = this_services.exclude(id=this_service.id)
            outdated_srvs.delete()
        else:
            #If there is only one, then take thre first
            this_service = this_services.first()
        #New request have this flag true
        if(add_this_service):
            #Booking has been updated with this request 
            if(has_booking_updated):
                #Does this service has an employee tagged already - then push for review
                if(this_service.employee != None):
                    this_service.review = True
                    this_service.save()
        else:
            #this service is no longer required - DONOT delete permanantly - these all are required for rate calculation
            this_service.retired = True
            this_service.save()