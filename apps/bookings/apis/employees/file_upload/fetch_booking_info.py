from lens35.constanst import CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER, EMPLOYEES_BUCKET, EMPLOYEES_DP_FOLDER
from util.wasabi import get_presigned_url_to_access_object
from util.google_maps import get_distance_bw_cordinates
from apps.employees.models.employees import Employees
from apps.bookings.models.bookings import Bookings
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['GET'])
def index(request, booking_id):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        booking = Bookings.objects.get(booking_id = booking_id)
        
        distance = get_distance_bw_cordinates((booking.event_latitude, booking.event_longitude), (employee.base_location_latitude, employee.base_location_longitude))
        services = []
        for service in Services.objects.filter(booking = booking).exclude(retired = True):
            employee = None
            if(service.employee != None):
                employee = {
                    "employee_id" : service.employee.employee_id, 
                    "full_name" : service.employee.full_name,
                    "profile_name" : service.employee.profile_name,
                    "display_picture" : __get_dp_url(service.employee.display_picture, "employee")
                }
            services.append({
                    "service_id" : service.service_id,
                    "service" : service.service,
                    "employee" : employee
                })

        response = {
                "booking_id" : booking.booking_id,
                "event" : booking.event,
                "event_date" : booking.event_date,
                "event_start_time" : booking.event_start_time,
                "event_duration" : booking.event_duration,
                "event_description" : booking.event_description,    
                "event_postal_code" : booking.event_postal_code,
                "event_city" : booking.event_city,
                "event_address" : booking.event_address,    
                "event_latitude" : booking.event_latitude,
                "event_longitude" : booking.event_longitude,
                "customer" : {
                    "customer_id" : booking.customer.customer_id,
                    "full_name" : booking.customer.full_name,
                    "mobile_number" : booking.customer.mobile_number,
                    "display_picture" :__get_dp_url(booking.customer.display_picture, "customer")
                },
                "services": services,
                "distance" : "{} Km".format(round(distance,1))
            }
        
        return build_response(200, "Success", response)
    except Exception as e_0:
        logger.error('Failed to fetch the bookings for employee {}\n{}'.format(employee_id, traceback.format_exc()))
        return build_response(400, str(e_0))
    

'''
#Function to get the display pic full url
'''
def __get_dp_url(file_name, user):
    if(file_name == None or file_name == ""):
        return None
    else:
        if(user == "employee"):
            return get_presigned_url_to_access_object(EMPLOYEES_BUCKET, EMPLOYEES_DP_FOLDER, file_name, "image/jpeg")
        if(user == "customer"):
            return get_presigned_url_to_access_object(CUSTOMERS_BUCKET, CUSTOMERS_DP_FOLDER, file_name, "image/jpeg")
        