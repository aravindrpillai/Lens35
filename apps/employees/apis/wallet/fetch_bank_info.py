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
            "has_bank_info" : False
        } if employee.bank_info == None else {
            "has_bank_info" : True,
            "bank_details_id" : employee.bank_info.bank_details_id,
            "bank" : employee.bank_info.bank,
            "branch" : employee.bank_info.branch,
            "ifsc" : employee.bank_info.ifsc,
            "account_holder" : employee.bank_info.account_holder,
            "mobile_number" : employee.bank_info.mobile_number
        }
        return build_response(200, "Success", resp)
    except Exception as e_0:
        logger.error('Failed to fetch Employee information : {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))
