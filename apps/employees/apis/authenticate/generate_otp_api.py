from lens35.constanst import SMS_OTP_LIMIT_PER_SESSION, SMS_RESEND_TIME_LIMIT_IN_MINUTES
from apps.employees.models.employee_otp import EmployeeOTP
from util.regex import validate_and_format_mobile_number
from rest_framework.decorators import api_view
from util.http import build_response
from django.utils import timezone
from util.logger import logger
from random import randrange
import traceback

@api_view(['POST'])
def index(request):
    try:
        mobile_number = validate_and_format_mobile_number(request.data.get("mobile_number", None))
        if(__is_request_within_limit(mobile_number=mobile_number)):
            otp = randrange(100001, 999999)
            __save_otp_info(mobile_number=mobile_number, otp=otp)
        else:
            return build_response(429, "OTP Limit Exceeded. Please try again after sometime")
        return build_response(201, None, {"otp_for_testing_purpose": otp}) #TODO - Remove sending OTP Back || Kept for testing
    except Exception as e_0:
        logger.error('Failed to push OTP : {}\n{}'.format(e_0, traceback.format_exc()))
        return build_response(400, str(e_0))


def __is_request_within_limit(mobile_number):
    #Below code gets the number of OTPs sent in the last 'n' minutes
    records_count = EmployeeOTP.objects.filter(
        mobile_number = mobile_number, 
        generated_time__gt = (timezone.now() - timezone.timedelta(minutes=SMS_RESEND_TIME_LIMIT_IN_MINUTES))
    ).count()
    return True if (records_count <= SMS_OTP_LIMIT_PER_SESSION) else False


def __save_otp_info(mobile_number, otp):
    emp_otp = EmployeeOTP()
    emp_otp.mobile_number = mobile_number
    emp_otp.otp = otp
    emp_otp.save()