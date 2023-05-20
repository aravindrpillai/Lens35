from apps.bookings.helper import create_lifecycle_event, create_service_invoice_item
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from django.utils import timezone
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, booking_id):
    try:
        if(booking_id == None or booking_id == ""):
            raise Exception("Booking cannot be empty.")
        customer_id = request.headers.get("Identifier")            
        
        services = Services.objects.filter(booking__booking_id = booking_id, booking__customer__customer_id = customer_id).exclude(retired = True)
        if(not services.exists()):
            raise Exception("No Services available")
        
        booking_date = services[0].booking.event_date
        if(booking_date <= timezone.now().date()):
            raise Exception("You cannot cancell or update bookings past event date")
            
        for service in services:
            service.retired = True
            service.lifecycle = [create_lifecycle_event("Removed {}".format(service.service))]
            create_service_invoice_item(service, "cancellation")
            service.save()
          
        return build_response(200, "Success", None)
    except Exception as e_0:
        logger.error('Failed to cancel booking {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))
