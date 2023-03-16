from util.regex import validate_and_format_email_id
from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.email_util import send_email
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        
        full_name = data.get("full_name", None)
        profile_name = data.get("profile_name", None)
        email_id = data.get("email_id", None)
        subscribe_for_updates = data.get("subscribe_for_updates", None)
        
        updated = False

        #Full name
        if(full_name != None and full_name != ""):
            employee.full_name = full_name
            updated = True

        #Profile Name
        if(profile_name != None and profile_name != "" and profile_name != employee.profile_name):
            emp = Employees.objects.filter(profile_name = profile_name).exclude(employee_id = employee.employee_id)
            if(emp.exists()):
                raise Exception("Profile name is already used")
            else:
                if(not profile_name.isalnum()):
                    raise Exception("profile name must not contain symbols or spaces")
                else:
                    employee.profile_name = profile_name.lower()
                    updated = True
            
        #Email ID
        if(email_id != None and email_id != "" and email_id != employee.email_id):
            email_id = validate_and_format_email_id(email_id)
            emp = Employees.objects.filter(email_id = email_id).exclude(employee_id = employee.employee_id)
            if(emp.exists()):
                raise Exception("This Email ID is already used")
            else:
                send_email("email_verification_template", {"employee_id":employee_id}, email_id)
                employee.email_id = email_id
                employee.email_id_verified = False
                updated = True
            
        #Subscribe for updates
        if(subscribe_for_updates != None and subscribe_for_updates != ""):
            employee.subscribe_for_updates = bool(subscribe_for_updates)
            updated = True
            
        if(updated):
            employee.save()

        response = {
            "full_name" : employee.full_name,
            "profile_name" : employee.profile_name,
            "email_id" : employee.email_id,
            "email_id_verified" : employee.email_id_verified,
            "subscribe_for_updates" : employee.subscribe_for_updates
        }
        message = "Successfully updated" if updated else "No changes to update"
        return build_response(202, message , response)
    
    except Exception as e_0:
        logger.error('Failed to update employee basic info %s - %s\n%s', employee_id, e_0, traceback.format_exc())
        return build_response(400, str(e_0))