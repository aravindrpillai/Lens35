#from apps.employees.helpers.authentication_helper import authenticate_api_request as auth_employee_token
from apps.customers.models.customer_token import CustomerToken
from apps.employees.models.employee_token import EmployeeToken
from lens35.constanst import TOKEN_EXPIRY_TIME_IN_MINUTES
from rest_framework.renderers import JSONRenderer
from datetime import datetime, timedelta
from util.http import build_response
from util.logger import logger
import traceback

'''
    Authentication Middleware
'''
class Authenticate():
    excluded_urls = [
      "employees/apis/generate/otp",
      "employees/apis/generate/token",
      "customers/apis/generate/otp",
      "customers/apis/generate/token",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __unauthorized_api_response(self):
        response = build_response(401, "Authentication Failed")
        response.content_type = "application/json"
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

    def __call__(self, request):
        full_path = request.get_full_path()
        for excluded_url in self.excluded_urls:
            if(excluded_url in full_path):
                return self.get_response(request)
        
        usertype = full_path.replace("https://", "").replace("http://", "").split('/')[1]
        usertype = usertype.lower()
        
        headers = request.headers
        token = headers.get('Token', None)
        identifier = headers.get('Identifier', None)
        device_id = headers.get('Device-Id', None)
        
        authenticated = self.__authorize(usertype, token, identifier, device_id)
        if(authenticated):
            return self.get_response(request)
        else:
            return self.__unauthorized_api_response()
 
    
    def __authorize(self, type, token, identifier, device_id):
        logger.debug("{} authorization info : {} | Identifier : {} | Device ID : {}".format(type, token, identifier, device_id))
        try:
            match type:
                case "customers":
                    tokens = CustomerToken.objects.filter(token = token, customer_id = identifier, device_id = device_id)    
                case "employees":
                    tokens = EmployeeToken.objects.filter(token = token, employee_id = identifier, device_id = device_id)    
                case __: 
                    return False

            if(tokens.exists()):
                token = tokens[0]
                if(token.keep_active):
                    logger.debug("KeepActive is true for this Token.")
                    return True
                else:
                    token_created_time = token.created_time
                    current_time = datetime.now(token_created_time.tzinfo)
                    token_valid = ((current_time - token_created_time) <= timedelta(minutes=TOKEN_EXPIRY_TIME_IN_MINUTES))
                    if(not token_valid):
                        logger.debug("Token is expired")
                        token.delete()
                        return False
                    else:
                        token.created_time = datetime.now(token_created_time.tzinfo)
                        logger.debug("Updated the token expiry")
                        token.save()
                        return True
            else:
                return False
        except Exception as e:        
            logger.error('%s\n%s', e, traceback.format_exc())
            return False