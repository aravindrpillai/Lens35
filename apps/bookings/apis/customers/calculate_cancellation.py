from apps.bookings.models.transactions import Transactions
from apps.bookings.models.services import Services
from lens35.constanst import CANCELLATION_CHARGE
from rest_framework.decorators import api_view
from util.http import build_response
from django.db.models import Sum, Q
from django.utils import timezone
from util.logger import logger
import traceback

'''
Cancellation Charge Calculation
    1. Pick all the services which are accepted by an employee. (ignore the non accepted services as cancellation charge is 0 for such services)
    2. Multiply the above count by CANCELLATION_CHARGE
    3. Get the aggregate amount from the transactions. This will tell you the total amount, the customer has paid. 
    4. Now substract (3) from (2) --> this will be the refund amount
'''
@api_view(['GET'])
def index(request, booking_id):
    try:
        if(booking_id == None or booking_id == ""):
            raise Exception("Booking cannot be empty.")
        customer_id = request.headers.get("Identifier")            
        
        total_cancellation_cost = 0
        service_list = []
        
        services = Services.objects.filter(booking__booking_id = booking_id, booking__customer__customer_id = customer_id).exclude(retired = True)
        if(not services.exists()):
            raise Exception("No Services available")
        
        booking_date = services[0].booking.event_date
        if(booking_date <= timezone.now().date()):
            raise Exception("You cannot cancell or update bookings past event date")
            
        for service in services:
            if(service.employee != None):
                total_cancellation_cost += CANCELLATION_CHARGE
            service_list.append({
                "service_name" : service.service,
                "employee" : None if service.employee == None else service.employee.full_name,
                "service_id" : service.service_id,
                "cancellation_cost" : 0 if service.employee == None else CANCELLATION_CHARGE
            })
        
         
        net_amount = Transactions.objects.filter(booking__booking_id=booking_id).aggregate(
            already_paid=Sum('amount', filter=~Q(reversed=True)),
            amount_reversed=Sum('amount', filter=Q(reversed=True))
        )
        already_paid_amount = net_amount['already_paid'] or 0
        amount_reversed = net_amount['amount_reversed'] or 0
        final_amount_paid = already_paid_amount - amount_reversed
        
        cancellation_data = {
            "services" : service_list,
            "total_cancellation_amount" : total_cancellation_cost,
            "paid_amount" : final_amount_paid,
            "refund_amount" : (final_amount_paid - total_cancellation_cost) 
        }  
        return build_response(202, "Success", cancellation_data)
    except Exception as e_0:
        logger.error('Failed to fetch invoice of booking {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))
