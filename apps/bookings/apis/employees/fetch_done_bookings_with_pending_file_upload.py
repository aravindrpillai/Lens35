from apps.bookings.models.bookings import Bookings
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        bookings = Bookings.objects.filter(services__employee__employee_id = employee_id).exclude(closed=True, retired=True)
        response_data = []
        services = []

        for service in booking.services:
            if((not (service.closed or service.retired)) and (employee_id == service.employee.employee_id)):
                services.append({
                    "service_id" : service.service_id,
                    "service" : service.service
                })

        for booking in bookings:
            response_data.append({
                "booking_id" : booking.booking_id,
                "event" : booking.event,
                "event_date" : booking.event_date,
                "event_start_time" : booking.event_start_time,
                "event_postal_code" : booking.event_postal_code,
                "event_city" : booking.event_city,
                "event_address" : booking.event_address,
                "customer_name" : booking.customer.full_name,
                "services": service
            })
        
        return build_response(200, None, response_data)
    except Exception as e_0:
        employee_id = request.headers.get("Identifier")
        logger.error('Failed to generate Presigned URL for {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))