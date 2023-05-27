from util.wasabi import delete_file_from_bucket, get_presigned_url_to_access_object
from lens35.constanst import CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER
from apps.customers.models.customers import Customers
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        customer_id = request.headers.get("Identifier")
        customer = Customers.objects.get(customer_id = customer_id)
        data = request.data
        file_name = data.get("file_name", None)

        if(customer.display_picture == file_name):
            link = None 
            if (customer.display_picture != None):
                link = get_presigned_url_to_access_object(CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER, customer.display_picture, "image/jpeg")
            return build_response(200, "No Change in DP", {"link": link})
        
        if(customer.display_picture != None):
            logger.debug("Deleting customer old profile picture as part of update - File: {}".format(customer.display_picture))
            delete_file_from_bucket(CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER, customer.display_picture)

        if(file_name == None or file_name == ""):
            customer.display_picture = None
            customer.save()
            return build_response(202, "DP removed successfully", {"link": None})
        else:
            customer.display_picture = file_name
            customer.save()
            new_link = get_presigned_url_to_access_object(CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER, file_name, "image/jpeg")
            return build_response(202, "DP updated successfully", {"link": new_link})
        
    except Exception as e_0:
        logger.error('Failed to update display picture for customer : {} - {}\n{}'.format(customer_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))