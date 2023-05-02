from apps.employees.models.employees import Employees
from util.regex import validate_and_format_pincode
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
from util.google_maps import get_cordinates
from .helper import update_account_status
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        
        base_location_pincode = data.get("base_location_pincode", None)
        base_location_city = data.get("base_location_city", None)
        if(base_location_pincode != None and base_location_pincode != "" and base_location_city != None and base_location_city != ""):
            pincode = validate_and_format_pincode(base_location_pincode)
            employee.base_location_pincode = pincode 
            employee.base_location_city = base_location_city
            address = "{}, {}".format(base_location_city, pincode)
            cord = get_cordinates(address)
            employee.base_location_latitude = cord[0]
            employee.base_location_longitude = cord[1]
            update_account_status(employee)
            employee.save()
        else:
            raise Exception("PostalCode and City must be available together")
        
        response = {
            "base_location_pincode" : employee.base_location_pincode,
            "base_location_city" : employee.base_location_city,
            "base_location_latitude" : employee.base_location_latitude,
            "base_location_longitude" : employee.base_location_longitude
        }
        return build_response(202, "Success", response)
    except Exception as e_0:
        logger.error('Failed to update employee base location {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))

