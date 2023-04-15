from lens35.constanst import EMPLOYEES_BUCKET, EMPLOYEES_DP_FOLDER, EMPLOYEES_ID_PROOF_FOLDER
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
        document_type = data.get("document_type", None)
        mime_type = data.get("mime_type", None)
        if(mime_type == None or mime_type == "" or (not mime_type.startswith('image/'))):
            raise Exception("Invalid File type. Please upload image files only")
        file_extension = mimetypes.guess_extension(mime_type, strict=False)

        if(document_type == None):
            raise Exception("Document type cannot be empty to rquest presigned URL")
        else:
            folder = None
            match document_type.lower():
                case "display_picture":
                    folder = EMPLOYEES_DP_FOLDER
                case "id_proof_front":
                    folder = EMPLOYEES_ID_PROOF_FOLDER
                case "id_proof_back" :
                    folder = EMPLOYEES_ID_PROOF_FOLDER
                case __:
                    raise Exception("Invalid document type. Type must be once amongst [display_picture, id_proof_front, id_proof_back]")
            file_name = "{}{}".format(uuid.uuid4(), file_extension)
            url_info = get_presigned_url_to_push_object(EMPLOYEES_BUCKET, folder, file_name)
            
            response = {
                "url" : url_info["url"],
                "connection_info": url_info["connection_info"],
                "file_name" : file_name,
                "document_type" : document_type
            }
            return build_response(200, None, response)
    except Exception as e_0:
        employee_id = request.headers.get("Identifier")
        logger.error('Failed to generate Presigned URL for {} [{}] - {}\n{}'.format(employee_id, document_type, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))