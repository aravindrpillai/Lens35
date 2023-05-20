from apps.bookings.helper import create_lifecycle_event, append_with_previous_lifecycle
from apps.bookings.apis.customers.fetch_services import fetch_services
from apps.bookings.models.services import Services
from apps.bookings.models.bookings import Bookings
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback
from uuid import UUID


#TODO --- VERIFY IF THIS SERVICE IS USED -- > REMOVING IS HANDLED AS PART OF ADD SERVICE ITSELF 
@api_view(['POST'])
def index(request):
    try:
        data = request.data
        booking_id = data.get("booking_id",None)
        booking = Bookings.objects.get(booking_id = UUID(booking_id, version=4))
        service_id_list = data.get("service_id_list",[])  
        count = 0  
        for service_id in service_id_list:
            services = Services.objects.filter(service_id = UUID(service_id, version=4), booking = booking)
            if(not services.exists()):
                raise Exception("Failed to fetch service with id : {}".format(service_id))
            service = services[0]
            service.retired = True
            service.lifecycle =  append_with_previous_lifecycle(service.lifecycle, create_lifecycle_event("Service Removed"))
            service.save()
            count += 1

        if(count > 0):
            life_cycle_event = create_lifecycle_event("{} services removed : ".format(count))
            booking.lifecycle = append_with_previous_lifecycle(booking.lifecycle, life_cycle_event)
            booking.save()

        return build_response(202, "Success", fetch_services(booking_id))
    except Exception as e_0:
        logger.error('Failed to remove services of booking {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))

