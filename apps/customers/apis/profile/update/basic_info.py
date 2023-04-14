from util.regex import validate_and_format_email_id
from apps.customers.models.customers import Customers
from rest_framework.decorators import api_view
from util.email_util import send_email
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        customer_id = request.headers.get("Identifier")
        customer = Customers.objects.get(customer_id = customer_id)
        data = request.data
        
        full_name = data.get("full_name", None)
        email_id = data.get("email_id", None)
        subscribe_for_updates = data.get("subscribe_for_updates", None)
        
        updated = False

        #Full name
        if(full_name != None and full_name != ""):
            customer.full_name = full_name
            updated = True

        #Email ID
        if(email_id != None and email_id != "" and email_id != customer.email_id):
            email_id = validate_and_format_email_id(email_id)
            cust = Customers.objects.filter(email_id = email_id).exclude(customer_id = customer.customer_id)
            if(cust.exists()):
                raise Exception("This Email ID is already used")
            else:
                #send_email("email_verification_template", {"customer_id":customer_id}, email_id)
                customer.email_id = email_id
                customer.email_id_verified = False
                updated = True
            
        #Subscribe for updates
        if(subscribe_for_updates != None and subscribe_for_updates != ""):
            customer.subscribe_for_updates = bool(subscribe_for_updates)
            updated = True
            
        if(updated):
            customer.save()

        response = {
            "full_name" : customer.full_name,
            "email_id" : customer.email_id,
            "email_id_verified" : customer.email_id_verified,
            "subscribe_for_updates" : customer.subscribe_for_updates
        }
        message = "Successfully updated" if updated else "No changes to update"
        return build_response(202, message , response)
    
    except Exception as e_0:
        logger.error('Failed to update customer basic info : {} - {}\n{}'.format(customer_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))