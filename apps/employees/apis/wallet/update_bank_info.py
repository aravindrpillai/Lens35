from apps.employees.models.employee_bank_details import EmployeeBankDetails
from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback
import uuid

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        
        bank = __validate_field("bank", data.get("bank", None))
        branch = __validate_field("branch", data.get("branch", None))
        ifsc = __validate_field("ifsc", data.get("ifsc", None))
        account_holder = __validate_field("account_holder", data.get("account_holder", None))
        mobile_number = data.get("mobile_number", None)

        print(bank+" -- "+branch+" -- "+ifsc+" -- "+account_holder+" -- "+mobile_number)

        bank_info = EmployeeBankDetails() if employee.bank_info == None else employee.bank_info
        bank_info.bank_details_id = uuid.uuid4() if employee.bank_info == None else bank_info.bank_details_id
        bank_info.bank = bank
        bank_info.branch = branch
        bank_info.ifsc = ifsc
        bank_info.account_holder = account_holder
        bank_info.mobile_number = mobile_number
        bank_info.save()
        employee.bank_info = bank_info
        employee.save()
        
        return build_response(200, "Success", None)
    except Exception as e_0:
        logger.error('Failed to fetch Employees bank information : {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))

def __validate_field(field, value):
    if(value == None or value == ""):
        raise Exception(field+" value cannot be empty")
    return value