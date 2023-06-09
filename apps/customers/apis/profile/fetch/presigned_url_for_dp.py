from lens35.constanst import CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER
from util.wasabi import get_presigned_url_to_push_object
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback
import mimetypes
import uuid

@api_view(['POST'])
def index(request):
    try:
        data = request.data

        mime_type = data.get("mime_type", None)
        if(mime_type == None or mime_type == "" or (not mime_type.startswith('image/'))):
            raise Exception("Invalid File type. Please upload image files only")
        file_extension = mimetypes.guess_extension(mime_type, strict=False)

        file_name = "{}.{}".format(uuid.uuid4(), file_extension)
        url_info = get_presigned_url_to_push_object(CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER, file_name)
        
        response = {
            "url" : url_info["url"],
            "connection_info": url_info["connection_info"],
            "file_name" : file_name,
        }
        return build_response(200, None, response)
    except Exception as e_0:
        employee_id = request.headers.get("Identifier")
        logger.error('Failed to generate Presigned URL for {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))