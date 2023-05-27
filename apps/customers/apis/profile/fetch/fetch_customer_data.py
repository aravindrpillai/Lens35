from lens35.constanst import CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER
from util.wasabi import get_presigned_url_to_access_object
from apps.customers.models.customers import Customers
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request):
    try:
        customer_id = request.headers.get("Identifier")
        customer = Customers.objects.get(customer_id = customer_id)
        
        resp = {
            "full_name": customer.full_name,
            "email_id": customer.email_id,
            "email_id_verified": customer.email_id_verified,
            "mobile_number": customer.mobile_number,
            "subscribe_for_updates" : customer.subscribe_for_updates,
            "display_picture": __get_dp_url(customer.display_picture),
        }
        return build_response(200, "Success", resp)
    except Exception as e_0:
        logger.error('Failed to fetch Employee information : {} - {}\n{}'.format(customer_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))


'''
#Function to get the display pic full url
'''
def __get_dp_url(file_name):
    if(file_name == None or file_name == ""):
        return None
    else:
        url = get_presigned_url_to_access_object(CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER, file_name, "image/jpeg")
        return url
