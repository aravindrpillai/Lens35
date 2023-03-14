from util.regex import validate_and_format_mobile_number, validate_and_format_otp, validate_and_format_bool, validate_and_format_uuid4
from apps.employees.models.employee_token import EmployeeToken
from apps.employees.models.employee_otp import EmployeeOTP
from apps.employees.models.employees import Employees
from lens35.constanst import SMS_OTP_EXPIRY_IN_MINUTES
from util.http import build_response, get_client_ip
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
from util.logger import logger
import traceback
import uuid

'''
#API method to make the authenticate and generate the token 
'''
@api_view(['POST'])
def index(request):
    try:
        data = request.data
        otp = validate_and_format_otp(data.get("otp", None))
        mobile_number = validate_and_format_mobile_number(request.data.get("mobile_number", None))
        
        # Define the time range
        now = timezone.now()
        expiry_time_delta = now - timedelta(minutes=SMS_OTP_EXPIRY_IN_MINUTES)
        otp_exist = EmployeeOTP.objects.filter(mobile_number=mobile_number, otp=otp, generated_time__gte=expiry_time_delta).exists()
        if(otp_exist):
            for otp in EmployeeOTP.objects.filter(mobile_number=mobile_number):
                otp.delete()
            employee_id = create_user_if_not_exist(mobile_number)
            ip_address = get_client_ip(request)
            device_id = validate_and_format_uuid4("device_id", data.get("device_id", None), True)
            keep_active = False if device_id == None else validate_and_format_bool("keep_active",data.get("keep_active", False))
            token = commit_token_data(employee_id, device_id, mobile_number, ip_address, keep_active)
            
            #Building the response
            response = {
                "Token" : token.token,
                "Device-Id":token.device_id,
                "Identifier":token.employee_id
            }
            return build_response(200, None, response)            
        else:
            return build_response(400, "Invalid/Expired OTP", None)
    except Exception as e_0:
        logger.error('Failed : %s\n%s', e_0, traceback.format_exc())
        return build_response(400, str(e_0))


'''
#Function to commit token data
'''
def commit_token_data(employee_id, device_id, mobile_number, ip_address, keep_active):
    try:
        tokens = EmployeeToken.objects.filter(mobile_number= mobile_number, device_id = device_id)
        for token in tokens:
            token.delete()
        tk = EmployeeToken()
        tk.mobile_number = mobile_number
        tk.device_id = uuid.uuid4() if (device_id == None) else device_id
        tk.employee_id = employee_id
        tk.token = uuid.uuid4()
        tk.ip_address = ip_address
        tk.keep_active = keep_active
        tk.save()
        return tk
    except Exception as e_0:
        logger.error('Failed to commit new token information: %s\n%s', e_0, traceback.format_exc())
        raise e_0


'''
#Function to create a new user
'''
def create_user_if_not_exist(mobile_number):
    try:
        emp = Employees.objects.get(mobile_number = mobile_number)
        return emp.employee_id
    except:
        logger.debug("Creating new Employee record")
        emp = Employees()
        emp.employee_id = uuid.uuid4()
        emp.mobile_number = mobile_number
        emp.save()
        return emp.employee_id