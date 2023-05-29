from util.wasabi import get_presigned_url_to_access_object
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from lens35.constanst import BOOKINGS_BUCKET
from apps.bookings.models.files import Files
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, service_id):
    try:
        employee_id = request.headers.get("Identifier")
        print("SERVUICE IS :: {}".format(service_id))
        service = Services.objects.get(service_id = service_id, employee__employee_id = employee_id)
        if(service.retired):
            raise Exception("Service Expired! Cannot pull data from this expired services.")
        
        files = Files.objects.filter(service = service)
        return_files = []
        for file in files:
            file_name_in_repo = str(file.file_id)+"."+file.file_name.split(".")[1]
            url = get_presigned_url_to_access_object(BOOKINGS_BUCKET, service_id, file_name_in_repo, file.mime_type)
            return_files.append({
                "url" : url,
                "file_id" : file.file_id,
                "file_name" : file.file_name,
                "mime_type" : file.mime_type
            })
            
        return build_response(200, None, return_files)
    except Exception as e_0:
        logger.error('Failed to fetch uploaded files : Emplyee id {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))