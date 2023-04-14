from lens35.constanst import SMS_OTP_EXPIRY_IN_MINUTES, TOKEN_EXPIRY_TIME_IN_MINUTES           
from apps.employees.models.employee_token import EmployeeToken
from apps.customers.models.customer_token import CustomerToken
from apps.employees.models.employee_otp  import EmployeeOTP
from apps.customers.models.customer_otp import CustomerOTP
from django.utils import timezone
from util.logger import logger
import traceback

def purge():
    try:
        logger.info("Starting to delete customer otps")
        __customer_otp()
        logger.info("Done customer otp deletion...")
    except Exception as e:
        logger.error('Failed to delete customer otps : {}\n{}'.format(e, traceback.format_exc()))

    try:
        logger.info("Starting to delete customer tokens")
        __customer_token()
        logger.info("Done customer token deletion...")
    except Exception as e:
        logger.error('Failed to delete customer tokens : {}\n{}'.format(e, traceback.format_exc()))

    try:
        logger.info("Starting to delete employee otps")
        __employee_otp()
        logger.info("Done employee otp deletion...")
    except Exception as e:
        logger.error('Failed to delete employee otps : {}\n{}'.format(e, traceback.format_exc()))

    try:
        logger.info("Starting to delete employee tokens")
        __employee_token()
        logger.info("Done employee token deletion...")
    except Exception as e:
        logger.error('Failed to delete employee tokens {}\n{}'.format(e, traceback.format_exc()))


def __customer_otp():
    sms_validity = timezone.now() - timezone.timedelta(minutes=SMS_OTP_EXPIRY_IN_MINUTES)
    records = CustomerOTP.objects.filter(generated_time__lte=sms_validity)
    for record in records:
        try:
            record.delete()
        except Exception as e:
            logger.error('Failed to delete customer otp {} : {}\n{}'.format(record, e, traceback.format_exc()))

def __employee_otp():
    sms_validity = timezone.now() - timezone.timedelta(minutes=SMS_OTP_EXPIRY_IN_MINUTES)
    records = EmployeeOTP.objects.filter(generated_time__lte=sms_validity)
    for record in records:
        try:
            record.delete()
        except Exception as e:
            logger.error('Failed to delete employee otp {} : {}\n{}'.format(record, e, traceback.format_exc()))

def __employee_token():
    token_validity = timezone.now() - timezone.timedelta(minutes=TOKEN_EXPIRY_TIME_IN_MINUTES)
    records = EmployeeToken.objects.filter(created_time__lte=token_validity)
    for record in records:
        try:
            record.delete()
        except Exception as e:
            logger.error('Failed to delete employee token {} : {}\n{}'.format(record, e, traceback.format_exc()))

def __customer_token():
    token_validity = timezone.now() - timezone.timedelta(minutes=TOKEN_EXPIRY_TIME_IN_MINUTES)
    records = CustomerToken.objects.filter(created_time__lte=token_validity)
    for record in records:
        try:
            record.delete()
        except Exception as e:
            logger.error('Failed to delete customer token {} : {}\n{}'.format(record, e, traceback.format_exc()))

