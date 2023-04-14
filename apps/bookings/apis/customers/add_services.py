from apps.bookings.helper import create_lifecycle_event, append_with_previous_lifecycle
from apps.bookings.apis.customers.fetch_services import fetch_services
from apps.bookings.models.bookings import Bookings
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback
import uuid

@api_view(['POST'])
def index(request):
    try:
        data = request.data

        booking_id = data.get("booking_id",None)
        booking = Bookings.objects.get(booking_id = booking_id)
        
        photographer_count = data.get("photography", 0)
        videographer_count = data.get("videography", 0)
        drone_photographer_count = data.get("drone_photography", 0)
        photo_editor_count = data.get("photo_editing", 0)
        video_editor_count = data.get("video_editing", 0)

        if(photo_editor_count > 1 or video_editor_count > 1):
            raise Exception("Photo/Video Editors cannot be more than 1")
        else:
            if(photo_editor_count > 0 and Services.objects.filter(booking = booking, service="photo_editor").exclude(retired = False).exists()):
                photo_editor_count = 0
                logger.debug("Photo Editor already exists in this booking. {}".format(booking_id))
            if(video_editor_count > 0 and Services.objects.filter(booking = booking, service="video_editor").exclude(retired = False).exists()):
                video_editor_count = 0
                logger.debug("Photo Editor already exists in this booking. {}".format(booking_id))
        
        if(photographer_count != None and photographer_count != "" and photographer_count > 0):
            __create_service(booking, "photography", photographer_count)
           
        if(videographer_count != None and videographer_count != "" and videographer_count > 0):
            __create_service(booking, "videography", videographer_count)
           
        if(drone_photographer_count != None and drone_photographer_count != "" and drone_photographer_count > 0):
            __create_service(booking, "drone_photography", drone_photographer_count)
           
        if(photo_editor_count != None and photo_editor_count != "" and photo_editor_count > 0):
            __create_service(booking, "photo_editing", 1)
           
        if(video_editor_count != None and video_editor_count != "" and video_editor_count > 0):
            __create_service(booking, "video_editing", 1)
           
        if(photographer_count > 0 or videographer_count > 0 or drone_photographer_count > 0 or photo_editor_count > 0 or video_editor_count > 0):
            life_cycle_event = create_lifecycle_event("Service Added - Photographer : {}, Videographer : {}, Drone Photographer : {}, Photo Editor : {}, Video Editor : {}, ".format(photographer_count, videographer_count, drone_photographer_count, photo_editor_count, video_editor_count))
            booking.lifecycle = append_with_previous_lifecycle(booking.lifecycle, life_cycle_event)
            booking.save()

        return build_response(202, "Success", fetch_services(booking_id))
    except Exception as e_0:
        logger.error('Failed to add new services to booking : {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))

    
def __create_service(booking, type, count):
    for i in range(0, count):
        service = Services()
        service.service_id = uuid.uuid4()
        service.booking = booking
        service.service = type
        service.lifecycle = [create_lifecycle_event("Created {}".format(type))]
        service.save()