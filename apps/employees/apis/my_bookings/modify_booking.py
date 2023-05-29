from lens35.constanst import EMPLOYEE_SERVICE_CANCELLATION_CHARGE
from apps.employees.models.employees import Employees
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        data = request.data
        booking_id = data.get("booking_id", None)
        new_service_ids = data.get("service_ids", [])
        
        employee = Employees.objects.get(employee_id = employee_id)
        my_services = Services.objects.filter(booking__booking_id=booking_id, employee=employee).exclude(retired=True, closed=True)
        services_to_delink = [ms for ms in my_services if ms.service_id not in new_service_ids]

        for delink_service in services_to_delink:
            delink_service.employee = None
            delink_service.save()
        for new_service_id in new_service_ids:
            service = Services.objects.get(booking__booking_id=booking_id, service_id=new_service_id)
            if(service.employee == None):
                service.employee = employee
                service.save()
        return build_response(200, "Success", None)
    except Exception as e_0:
        logger.error('Failed to fetch the bookings for employee {}\n{}'.format(employee_id, traceback.format_exc()))
        return build_response(400, str(e_0))