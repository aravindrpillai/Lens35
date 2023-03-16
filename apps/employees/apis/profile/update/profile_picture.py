from util.wasabi import delete_file_from_bucket, get_presigned_url_to_access_object
from lens35.constanst import EMPLOYEES_BUCKET, EMPLOYEES_DP_FOLDER
from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        file_name = data.get("file_name", None)

        if(employee.display_picture == file_name):
            link = None 
            if (employee.display_picture != None):
                link = get_presigned_url_to_access_object(EMPLOYEES_BUCKET, EMPLOYEES_DP_FOLDER, employee.display_picture)
            return build_response(200, "No Change in DP", {"link": link})
        
        if(file_name == None or file_name == ""):
            employee.display_picture = None
            employee.save()
            return build_response(202, "DP removed successfully", {"link": None})
        else:
            employee.display_picture = file_name
            employee.save()
            new_link = get_presigned_url_to_access_object(EMPLOYEES_BUCKET, EMPLOYEES_DP_FOLDER, file_name)
            return build_response(202, "DP updated successfully", {"link": new_link})
        
    except Exception as e_0:
        logger.error('Failed to update display picture for employee %s - %s\n%s', employee_id, e_0, traceback.format_exc())
        return build_response(400, str(e_0))