from apps.customers.models.customers import Customers
from rest_framework.decorators import api_view
from util.http import build_response
from util.encryption import decrypt
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, token):
    try:
        email_id = None
        customer_id = None
        decrypted_data = decrypt(token)
        data_split = decrypted_data.split("#")
        customer_id = data_split[0]
        email_id = data_split[1]
        customer = Customers.objects.get(customer_id = customer_id, email_id=email_id)
        customer.email_id_verified = True
        customer.save()
        return build_response(202, "Success" , {"full_name" : customer.full_name})
    except Exception as e_0:
        logger.error('Failed to verify email {}: for customer {} - {}\n{}'.format(email_id, customer_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))