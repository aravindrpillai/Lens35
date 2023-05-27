from util.wasabi import get_presigned_url_to_access_object
from rest_framework.decorators import api_view
from lens35.constanst import BOOKINGS_BUCKET
from apps.bookings.models.files import Files
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, service_id):
    try:
        customer_id = request.headers.get("Identifier")
        response = []
        files = Files.objects.filter(service__service_id = service_id, service__booking__customer__customer_id = customer_id)
        for file in files:
            file_name_in_repo = str(file.file_id)+"."+file.file_name.split(".")[1]
            url = get_presigned_url_to_access_object(BOOKINGS_BUCKET, service_id, file_name_in_repo, file.mime_type)
            response.append({
                "file_id" : file.file_id,
                "file_name" : file.file_name,
                "url" : url,
                "mime_type" : file.mime_type
            })
        return build_response(200, "Success", response)
    except Exception as e_0:
        logger.error('Failed to fetch files of services {}\n{}'.format(service_id, traceback.format_exc()))
        return build_response(400, str(e_0))
