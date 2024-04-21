from lens35.constanst import PHOTOGRAPHER_RATE_PER_HOUR, VIDEOGRAPHER_RATE_PER_HOUR, DRONE_RATE_PER_HOUR
from apps.bookings.models.service_invoice_items import ServiceInvoiceItems
from apps.customers.apis.bookings.fetch_services import fetch_services
from apps.customers.helper import create_lifecycle_event
from apps.bookings.models.bookings import Bookings
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from django.db.models import Q
from util.logger import logger
import traceback
import uuid


@api_view(['POST'])
def index(request):
    try:
        data = request.data
        customer_id = request.headers.get("Identifier")   
        booking_id = data.get("booking_id",None)
        booking = Bookings.objects.get(booking_id = booking_id)
        if(booking.published):
            logger.error('This service cannot be used for bookings that are published: BookingID {}'.format(booking_id))
            return build_response(400, "This service cannot be used for bookings that are published", None)

        photographer = data.get("photography", False)
        videographer = data.get("videography", False)
        drone = data.get("drone", False)

        #flush all prior services
        Services.objects.filter(booking = booking).delete()
        
        if(photographer):
            __handle_service(booking, "photography")
        if(videographer):
            __handle_service(booking, "videography")
        if(drone):
            __handle_service(booking, "drone")
        
        return build_response(202, "Success", fetch_services(booking_id, customer_id))
    except Exception as e_0:
        logger.error('Failed to add/update services to booking : {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))

    
def __handle_service(booking, service_name):
    try:
        service = Services()
        service.service_id = uuid.uuid4()
        service.booking = booking
        service.service = service_name
        service.lifecycle = [create_lifecycle_event("Created new service: {}".format(service_name))]
        service.save()
        logger.info('Add {} service to booking : {}'.format(service_name, booking.booking_id))
        __handle_charges(booking, service)
    except Exception as e_0:
        logger.error('Failed to add {} service to booking : {}\n{}'.format(service_name, booking.booking_id, traceback.format_exc()))
        raise e_0


def __handle_charges(booking, service):
    service_charge = 0
    event_duration = booking.event_duration
    match service.service:
        case "photography" : 
            service_charge = PHOTOGRAPHER_RATE_PER_HOUR             
        case "videography" : 
            service_charge = VIDEOGRAPHER_RATE_PER_HOUR
        case "drone" : 
            service_charge = DRONE_RATE_PER_HOUR
        case __ : raise Exception("Failed to rate the service. invalid service code")

    service_invoice_item = ServiceInvoiceItems()
    service_invoice_item.invoice_item_id = uuid.uuid4()
    service_invoice_item.service = service
    service_invoice_item.cost = (event_duration * service_charge)
    service_invoice_item.cost_category = "booking_cost"
    desc = "New Service charge for {}. ({}Hrs x Rs.{} = {})".format(service.service.capitalize(), event_duration, service_charge, event_duration*service_charge)
    service_invoice_item.description = desc
    service_invoice_item.save()
    logger.info('Service charge added to service {} on booking {}'.format(service.service, booking.booking_id))
        