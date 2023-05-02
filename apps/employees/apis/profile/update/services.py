from apps.employees.models.employees import Employees
from util.regex import validate_and_format_bool
from rest_framework.decorators import api_view
from .helper import update_account_status
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        
        is_photographer = validate_and_format_bool("is_photographer",data.get("is_photographer", None))
        is_videographer = validate_and_format_bool("is_videographer",data.get("is_videographer", None))
        is_drone_photographer = validate_and_format_bool("is_drone_photographer",data.get("is_drone_photographer", None))
        is_photo_editor = validate_and_format_bool("is_photo_editor",data.get("is_photo_editor", None))
        is_video_editor = validate_and_format_bool("is_video_editor",data.get("is_video_editor", None))
        
        if all([not is_photographer, not is_videographer, not is_drone_photographer, not is_photo_editor, not is_video_editor]):
            raise Exception("Atlease one service must be added")     
        
        employee.is_photographer = is_photographer
        employee.is_videographer = is_videographer
        employee.is_drone_photographer = is_drone_photographer
        employee.is_photo_editor = is_photo_editor
        employee.is_video_editor = is_video_editor
        update_account_status(employee)
        employee.save()

        response = {
            "is_photographer" : employee.is_photographer,
            "is_videographer" : employee.is_videographer,
            "is_drone_photographer" : employee.is_drone_photographer,
            "is_photo_editor" : employee.is_photo_editor,
            "is_video_editor" : employee.is_video_editor  
        }

        return build_response(202, "Successfully updated the services", response)
    except Exception as e_0:
        logger.error('Failed to update services for employee : {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))
    