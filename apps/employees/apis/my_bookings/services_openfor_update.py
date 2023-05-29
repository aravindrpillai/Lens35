from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from django.db.models import Q
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, booking_id):
    try:
        employee_id = request.headers.get("Identifier")
        
        services = Services.objects.filter(
            Q(booking__booking_id=booking_id) & 
            (Q(employee__employee_id=employee_id) | Q(employee__employee_id__isnull=True))).exclude(retired=True, closed=True)
        if(not services.exists()):
            raise Exception("No available services to modify")
        
        response = [
            {
                "service_id": service.service_id,
                "service": service.service,
                "is_still_open": service.employee is None
            }
            for service in services
        ]

        return build_response(200, "Success", response)
    except Exception as e_0:
        logger.error('Failed to fetch the bookings for employee {}\n{}'.format(employee_id, traceback.format_exc()))
        return build_response(400, str(e_0))