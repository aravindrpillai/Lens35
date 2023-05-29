from util.google_maps import get_distance_bw_cordinates
from apps.employees.models.employees import Employees
from apps.bookings.models.services import Services
from apps.bookings.models.bookings import Bookings
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
from datetime import datetime
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        
        event_date = data.get("event_date", None)
        if(event_date == None):
            raise Exception("Date cannot be empty")
        event_date_split = event_date.split("-")
        year = event_date_split[0]
        month = event_date_split[1]
        target_event_date = datetime.strptime(f'{year}-{month}', '%Y-%m')
        
        events_array = data.get("events", [])
        if(not events_array):
            raise Exception("Select atleast one service")

        photography = data.get("photography", None)# and employee.is_photographer
        videography = data.get("videography", None) #and employee.is_videographer
        drone_photography = data.get("drone_photography", None)# and employee.is_drone_photographer
        photo_editing = data.get("photo_editing", None) #and employee.is_photo_editor
        video_editing = data.get("video_editing", None) #and employee.is_video_editor

        service_code_array = []
        if(photography):
            service_code_array.append("photography")
        if(videography):
            service_code_array.append("videography")
        if(drone_photography):
            service_code_array.append("drone_photography")
        if(photo_editing):
            service_code_array.append("photo_editing")
        if(video_editing):
            service_code_array.append("video_editing")
        if(not service_code_array):
            raise Exception("No service selected")
        
        bookings = Bookings.objects.filter(event__in=events_array, services__service__in=service_code_array, event_date__year=target_event_date.year, event_date__month=target_event_date.month).distinct()
        
        response = []
        done_booking_id = []
        for booking in bookings:
            services = Services.objects.filter(booking = booking, employee = employee).exclude(retired = True).values_list('service', flat=True).distinct()
            if(not services.exists()):
                continue
            distance = get_distance_bw_cordinates((booking.event_latitude, booking.event_longitude), (employee.base_location_latitude, employee.base_location_longitude))
            response.append({
                "booking_id" : booking.booking_id,
                "event" : booking.event,
                "event_date" : booking.event_date,
                "event_start_time" : booking.event_start_time,
                "event_duration" : booking.event_duration,
                "services": list(services),
                "distance" : "{} Km".format(round(distance,1)),
                "customer_name" : booking.customer.full_name,
                "customer_contact" : booking.customer.mobile_number,
            })
            done_booking_id.append(booking.booking_id)

        return build_response(200, "Success", response)
    except Exception as e_0:
        logger.error('Failed to fetch the bookings for employee {}\n{}'.format(employee_id, traceback.format_exc()))
        return build_response(400, str(e_0))