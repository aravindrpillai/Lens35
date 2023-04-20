from util.wasabi import get_presigned_url_to_push_object, create_folder_inside_bucket
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from apps.bookings.models.files import Files
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        data = request.data

        employee_id = request.headers.get("Identifier")
        service_id = data.get("service_id", None)
        mime_type = data.get("mime_type", None)
        file_name = data.get("file_name", None)
        
        service = Services.objects.get(service_id = service_id, employee__employee_id = employee_id)
        if(service.retired):
            raise Exception("Cannot upload to this service. Service is expired")
        
        file = Files()
        file.service = service
        file.file_name = file_name
        file.mime_type = mime_type
        file.save()
        
        return build_response(200, "Acknodwledged", None)
    except Exception as e_0:
        logger.error('Failed to acknodwledge file upload : Emplyee id {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))