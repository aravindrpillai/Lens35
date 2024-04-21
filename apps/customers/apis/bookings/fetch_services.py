from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, booking_id):
    try:
        customer_id = request.headers.get("Identifier")       
        response = fetch_services(booking_id, customer_id)
        return build_response(202, "Success", response)
    except Exception as e_0:
        logger.error('Failed to fetch the services of booking {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))

#Below function is called from add and remove apis as well
def fetch_services(booking_id, customer_id):
    
    response = []
    services = Services.objects.filter(booking__booking_id = booking_id, booking__customer__customer_id=customer_id).exclude(retired = True)
    if(not services.exists()):
        return response
    for service in services:
        employee = {
                "employee_id" : service.employee.employee_id,
                "full_name" : service.employee.full_name,
                "profile_name" : service.employee.profile_name,
                "display_picture" : service.employee.display_picture
            } if service.employee != None else None
        response.append({
            "service" : service.service,
            "service_id" : service.service_id,
            "created_time" : str(service.created_time),
            "employee" : employee,
            "closed" : service.closed,
            "review" : service.review
        })
    return response

    
