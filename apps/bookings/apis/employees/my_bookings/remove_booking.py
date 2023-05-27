from apps.employees.models.employees import Employees
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
from uuid import UUID
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        
        data = request.data
        booking_id = data.get("booking_id",None)
        sid_list = data.get("service_id_list",None)
        service_id_list = []
        for sid in sid_list:
            service_id_list.append(UUID(sid))
        services = Services.objects.filter(booking__booking_id = booking_id, service_id__in = service_id_list).exclude(retired=True)
        
        if(len(services) != len(sid_list)):
             raise Exception("Invalid service id found in the request")
        
        for service in services:
            if(service.employee == employee):
                service.employee = None
                service.save()
            else: 
                raise Exception("{} service '{}' is not your booking".format(service.service, service.service_id))
        return build_response(202, "Success", None)
    except Exception as e_0:
        logger.error('Failed to remove booking/service for employee {}\n{}'.format(employee_id, traceback.format_exc()))
        return build_response(400, str(e_0))
    