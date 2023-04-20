from apps.bookings.models.bookings import Bookings
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback
import json

@api_view(['GET'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        added_bookings = []
        bookings = Bookings.objects.filter(services__employee__employee_id = employee_id).exclude(services__closed=True).exclude(services__retired=True)
        response_data = []
        for booking in bookings:
            if(not (booking.booking_id in added_bookings)):
                services = []
                for service in Services.objects.filter(booking=booking, employee__employee_id = employee_id).exclude(closed=True).exclude(retired=True):
                    services.append({
                        "service_id" : service.service_id,
                        "service" : service.service
                    })
                response_data.append({
                    "booking_id" : booking.booking_id,
                    "event" : booking.event,
                    "event_date" : booking.event_date,
                    "event_start_time" : booking.event_start_time,
                    "event_postal_code" : booking.event_postal_code,
                    "event_city" : booking.event_city,
                    "event_address" : booking.event_address,
                    "customer_name" : booking.customer.full_name,
                    "services": services
                })
                added_bookings.append(booking.booking_id)
        return build_response(200, None, response_data)
    except Exception as e_0:
        logger.error('Failed to fetch completion pending booking for {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))
        
        