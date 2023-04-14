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
            if((service.service == "photography" and employee.is_photographer)
                or (service.service == "videography" and employee.is_videographer)
                or (service.service == "drone_photography" and employee.is_drone_photographer)
                or (service.service == "photo_editing" and employee.is_photo_editor)
                or (service.service == "video_editing" and employee.is_video_editor)):
                    if(service.employee != None and service.employee != employee):
                         raise Exception("{} service '{}' under booking {} is already booked".format(service.service, service.service_id, booking_id))
                    if(service.employee != employee):
                        service.employee = employee
                        service.save()
            else: 
                raise Exception("Employee is not registered to accept {} bookings".format(service.service))

        return build_response(202, "Success", None)
    except Exception as e_0:
        logger.error('Failed to accept booking for employee {}\n{}'.format(employee_id, traceback.format_exc()))
        return build_response(400, str(e_0))
    