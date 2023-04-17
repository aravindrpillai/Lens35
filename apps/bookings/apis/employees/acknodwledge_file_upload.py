from util.wasabi import get_presigned_url_to_push_object, create_folder_inside_bucket
from apps.bookings.models.bookings import Bookings
from rest_framework.decorators import api_view
from lens35.constanst import BOOKINGS_BUCKET
from util.http import build_response
from util.logger import logger
import traceback
import mimetypes
import uuid

@api_view(['POST'])
def index(request):
    try:
        data = request.data

        employee_id = request.headers.get("Identifier")
        service_id = data.get("service_id", None)
        mime_type = data.get("mime_type", None)
        file_name = data.get("file_name", None)
        uploaded = data.get("file_name", None)
        
        response = {
            "development_pending" : "yes_sir"
        }
        return build_response(200, None, response)
    except Exception as e_0:
        logger.error('Failed to acknodwledge file upload : Emplyee id {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))