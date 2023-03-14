from rest_framework.response import Response
from lens35.settings import CORS_ALLOWED_ORIGINS, CUSTOM_HEADERS

'''
# Function to get the client IP from request
# Metohd : NONE
'''
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


'''
# Function to build the response
# Metohd : NONE
'''
def build_response(response_code, message, data=None):
    if (hasattr(message, '__len__') and (not isinstance(message, str))):
        pass
    else:
        message = [message]
    fdata = {
        "status" : True if response_code < 300 else False,
        "messages" : message,
        "data" :data
    }
    resp =  Response(fdata, response_code)
    
    cust_headers = (','.join(str(each_hdr) for each_hdr in CUSTOM_HEADERS))
    allowed_origins = (','.join(str(each_origin) for each_origin in CORS_ALLOWED_ORIGINS))
    
    resp['Access-Control-Allow-Origin'] = "*"
    resp["Access-Control-Allow-Headers"] = 'X-Requested-With, Content-Type, '+cust_headers
    return resp