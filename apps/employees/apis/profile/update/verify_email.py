from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.http import build_response
from util.encryption import decrypt
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, token):
    try:  
        email_id = None
        employee_id = None
        decrypted_data = decrypt(token)
        data_split = decrypted_data.split("#")
        employee_id = data_split[0]
        email_id = data_split[1]
        employee = Employees.objects.get(employee_id = employee_id, email_id=email_id)
        employee.email_id_verified = True
        employee.save()
        return build_response(202, "Success" , {"full_name" : employee.full_name})
    except Exception as e_0:
        logger.error('Failed to verify email {}: for employee {} - {}\n{}'.format(email_id, employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))