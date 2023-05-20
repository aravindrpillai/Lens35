from apps.bookings.helper import create_lifecycle_event, append_with_previous_lifecycle, create_service_invoice_item
from apps.bookings.apis.customers.fetch_services import fetch_services
from apps.bookings.models.bookings import Bookings
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from django.db.models import Q
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
            if(photo_editor_count > 0 and Services.objects.filter(booking = booking, service="photo_editor").exclude(Q(retired=True) | Q(closed=True)).exists()):
                photo_editor_count = 0
                logger.debug("Photo Editor already exists in this booking. {}".format(booking_id))
            if(video_editor_count > 0 and Services.objects.filter(booking = booking, service="video_editor").exclude(Q(retired=True) | Q(closed=True)).exists()):
                video_editor_count = 0
                logger.debug("Photo Editor already exists in this booking. {}".format(booking_id))
        
        if(photographer_count != None and photographer_count != ""):
            __create_service(booking, "photography", photographer_count)
           
        if(videographer_count != None and videographer_count != ""):
            __create_service(booking, "videography", videographer_count)
           
        if(drone_photographer_count != None and drone_photographer_count != ""):
            __create_service(booking, "drone_photography", drone_photographer_count)
           
        if(photo_editor_count != None and photo_editor_count != ""):
            __create_service(booking, "photo_editing", photo_editor_count)
           
        if(video_editor_count != None and video_editor_count != ""):
            __create_service(booking, "video_editing", photo_editor_count)

        if(photographer_count > 0 or videographer_count > 0 or drone_photographer_count > 0 or photo_editor_count > 0 or video_editor_count > 0):
            life_cycle_event = create_lifecycle_event("Service Added - Photographer : {}, Videographer : {}, Drone Photographer : {}, Photo Editor : {}, Video Editor : {}, ".format(photographer_count, videographer_count, drone_photographer_count, photo_editor_count, video_editor_count))
            booking.lifecycle = append_with_previous_lifecycle(booking.lifecycle, life_cycle_event)
            booking.save()

        return build_response(202, "Success", fetch_services(booking_id))
    except Exception as e_0:
        logger.error('Failed to add new services to booking : {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))

    
def __create_service(booking, service_type, count_in_request):
    existing_services = Services.objects.filter(booking = booking, service=service_type).exclude(Q(retired=True) | Q(closed=True))
    existing_services_count = existing_services.count()
    new_count = count_in_request - existing_services_count
    #If new_count = 0, means there is no update on this service 
    if(new_count == 0):
        return
    
    #If new_count is < 0, means the request came in is to remove the services.
    if (new_count < 0):
        delete_flag = (new_count*-1)
        
        #First remove the services that ARE NOT ACCEPTED by the employee
        open_bookings = Services.objects.filter(booking = booking, service=service_type, employee=None).exclude(Q(retired=True) | Q(closed=True))
        for service in open_bookings:
            if(delete_flag < 1):
                break
            #We dont need to retire services that are not tagged to an employee - hence deleting it completely
            service.delete()
            delete_flag -= 1

        #Then remove the services that ARE ACCEPTED by the employee
        if(delete_flag < 1):
            return
        accepted_bookings = Services.objects.filter(booking = booking, service=service_type).exclude(employee=None).exclude(Q(retired=True) | Q(closed=True))
        for service in accepted_bookings:
            if(delete_flag < 1):
                break
            service.retired = True
            service.lifecycle = [create_lifecycle_event("Removed {}".format(service_type))]
            create_service_invoice_item(service, "cancellation")
            delete_flag -= 1
            service.save()
        
    else:
        for i in range(0, new_count):
            service = Services()
            service.service_id = uuid.uuid4()
            service.booking = booking
            service.service = service_type
            service.lifecycle = [create_lifecycle_event("Created {}".format(service_type))]
            service.save()
            try:
                create_service_invoice_item(service, "booking_cost")
            except Exception as e_0:
                service.delete()
                raise e_0
