from lens35.constanst import EMPLOYEES_BUCKET, EMPLOYEES_DP_FOLDER, EMPLOYEES_ID_PROOF_FOLDER
from util.wasabi import get_presigned_url_to_access_object
from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        
        resp = {
            "full_name": employee.full_name,
            "profile_name": employee.profile_name,
            "email_id": employee.email_id,
            "email_id_verified": employee.email_id_verified,
            "mobile_number": employee.mobile_number,
            "subscribe_for_updates" : employee.subscribe_for_updates,
            "display_picture": __get_file_url(employee.display_picture, "display_picture"),
            "id_proof_front": __get_file_url(employee.id_proof_front, "id_proof"),
            "id_proof_back": __get_file_url(employee.id_proof_back, "id_proof"),
            "id_proof_type": employee.id_proof_type,
            "base_location_city" : employee.base_location_city,
            "base_location_pincode" : employee.base_location_pincode,
            "portfolios":employee.portfolios,
            "is_photographer" : employee.is_photographer,
            "is_videographer" : employee.is_videographer,
            "is_drone_photographer" : employee.is_drone_photographer,
            "is_photo_editor" : employee.is_photo_editor,
            "is_video_editor" : employee.is_video_editor
        }
        return build_response(200, "Success", resp)
    except Exception as e_0:
        logger.error('Failed to fetch Employee information %s - %s\n%s', employee_id, e_0, traceback.format_exc())
        return build_response(400, str(e_0))


'''
#Function to get the display pic full url
'''
def __get_file_url(file_name, type):
    if(file_name == None or file_name == ""):
        return None
    else:
        folder = EMPLOYEES_DP_FOLDER if (type == "display_picture") else EMPLOYEES_ID_PROOF_FOLDER
        url = get_presigned_url_to_access_object(EMPLOYEES_BUCKET, folder.value, file_name)
        return url
