from util.wasabi import get_presigned_url_to_push_object, create_folder_inside_bucket
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from lens35.constanst import BOOKINGS_BUCKET
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
        is_photo = data.get("is_photo", None)

        service = Services.objects.get(service_id = service_id, employee__employee_id = employee_id)
        if(service.retired):
            raise Exception("Cannot upload to this service. Service is expired")
        
        # if(mime_type == None or mime_type == "" or (not mime_type.startswith('image/'))):
        #     raise Exception("Invalid File type. Please upload image files only")
        # file_extension = mimetypes.guess_extension(mime_type, strict=False)

        create_folder_inside_bucket(BOOKINGS_BUCKET, service_id)
        
        url_info = get_presigned_url_to_push_object(BOOKINGS_BUCKET, service_id, file_name)
        
        response = {
            "url" : url_info["url"],
            "connection_info": url_info["connection_info"],
            "file_name" : file_name
        }
        return build_response(200, None, response)
    except Exception as e_0:
        employee_id = request.headers.get("Identifier")
        logger.error('Failed to generate Presigned URL for {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))