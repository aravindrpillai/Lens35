from apps.bookings.models.services import Services
from apps.bookings.models.files import Files
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, service_id):
    try:
        employee_id = request.headers.get("Identifier")
        service = Services.objects.get(service_id = service_id, employee__employee_id = employee_id)
        files_exists = Files.objects.filter(service = service).exists()
        if(not files_exists):
            raise Exception("Cannot lock this services. No files uploaded to this service.")
        if(service.retired):
            raise Exception("This service is expired")
        service.closed = True 
        service.save()
           
        return build_response(200, "Locked", None)
    except Exception as e_0:
        logger.error('Failed to lock the service : Service id {} - {}\n{}'.format(service_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))