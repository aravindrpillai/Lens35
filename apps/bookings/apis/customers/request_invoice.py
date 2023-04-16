from apps.bookings.models.service_invoice import ServiceInvoice
from apps.bookings.models.transactions import Transactions
from rest_framework.decorators import api_view
from django.db.models import Count, Sum
from util.http import build_response
from util.logger import logger
from uuid import UUID
import traceback

@api_view(['GET'])
def index(request, booking_id):
    try:
        if(booking_id == None or booking_id == ""):
            raise Exception("Booking cannot be empty.")
        customer_id = request.headers.get("Identifier")            
        invoice_items = []
        total_amount = 0
        service_invoices = ServiceInvoice.objects.filter(service__booking__booking_id = booking_id, service__booking__customer__customer_id = customer_id).exclude(service__retired=True).values('service__service').annotate(final_amount=Sum('final_amount'))
        if(not service_invoices.exists()):
            raise Exception("Access denied. This booking is not associated to you")
            
        for invoice in service_invoices:
            total_amount += invoice['final_amount']
            invoice_items.append({
                "category" : "services",
                "service" : invoice['service__service'],
                "total_cost" : invoice['final_amount']
            })

        
        already_paid_amount = Transactions.objects.filter(booking__booking_id=booking_id).aggregate(Sum('amount'))['amount__sum']
        
        if (already_paid_amount == None):
            already_paid_amount = 0
        
        invoice = {
            "invoice_items" : invoice_items,
            "total_service_amount" : total_amount,
            "paid_amount" : already_paid_amount,
            "outstanding_amount" : (total_amount - already_paid_amount) 
        }  
        return build_response(202, "Success", invoice)
    except Exception as e_0:
        logger.error('Failed to fetch invoice of booking {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))
