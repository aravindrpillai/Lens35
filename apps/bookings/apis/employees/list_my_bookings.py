from apps.employees.models.employees import Employees
from apps.bookings.models.services import Services
from apps.bookings.models.bookings import Bookings
from util.google_maps import get_distance_bw_cordinates
from rest_framework.decorators import api_view
from util.http import build_response
from django.utils import timezone
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
        event_date = timezone.now().date() if (event_date == None or event_date == "") else datetime.fromisoformat(event_date).date()
        
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
            if(employee.is_photographer):
                service_code_array.append("photography")
            if(employee.is_videographer):
                service_code_array.append("videography")
            if(employee.is_drone_photographer):
                service_code_array.append("drone_photography")
            if(employee.is_photo_editor):
                service_code_array.append("photo_editing")
            if(employee.is_video_editor):
                service_code_array.append("video_editing")
        
        bookings = Bookings.objects.filter(services__service__in=service_code_array, event_date = event_date).distinct()
        
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
                "distance" : "{} Km".format(round(distance,1))
            })
            done_booking_id.append(booking.booking_id)

        return build_response(200, "Success", response)
    except Exception as e_0:
        logger.error('Failed to fetch the bookings for employee {}\n{}'.format(employee_id, traceback.format_exc()))
        return build_response(400, str(e_0))