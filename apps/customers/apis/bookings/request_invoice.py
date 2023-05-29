from apps.bookings.models.service_invoice_items import ServiceInvoiceItems
from apps.bookings.models.transactions import Transactions
from apps.bookings.models.services import Services
from rest_framework.decorators import api_view
from util.http import build_response
from django.db.models import Sum, Q
from util.logger import logger
import traceback


@api_view(['GET'])
def index(request, booking_id):
    try:
        if(booking_id == None or booking_id == ""):
            raise Exception("Booking cannot be empty.")
        customer_id = request.headers.get("Identifier")            
        
        total_amount = 0
        service_list = []

        services = Services.objects.filter(booking__booking_id = booking_id, booking__customer__customer_id = customer_id)
        if(not services.exists()):
            raise Exception("No Services available")
        for service in services:
            service_cost = 0
            invoice_items = []
            service_invoices_items = ServiceInvoiceItems.objects.filter(service = service)
            for sii in service_invoices_items:
                total_amount += sii.cost
                service_cost += sii.cost
                invoice_items.append({
                    "invoice_item_id" : sii.invoice_item_id,
                    "category" : sii.cost_category,
                    "description" : sii.description,
                    "total_cost" : sii.cost
                })
            service_list.append({
                "service_name" : service.service,
                "employee" : None if service.employee == None else service.employee.full_name,
                "retired" : service.retired,
                "service_id" : service.service_id,
                "invoice_items" : invoice_items,
                "service_cost" : service_cost
            })
        
        net_amount = Transactions.objects.filter(booking__booking_id=booking_id).aggregate(
            already_paid=Sum('amount', filter=~Q(reversed=True)),
            amount_reversed=Sum('amount', filter=Q(reversed=True))
        )       
        already_paid_amount = net_amount['already_paid'] or 0
        amount_reversed = net_amount['amount_reversed'] or 0
        final_amount_paid = already_paid_amount - amount_reversed

        invoice = {
            "services" : service_list,
            "total_service_amount" : total_amount,
            "paid_amount" : final_amount_paid,
            "outstanding_amount" : (total_amount - final_amount_paid) 
        }  
        return build_response(202, "Success", invoice)
    except Exception as e_0:
        logger.error('Failed to fetch invoice of booking {}\n{}'.format(booking_id, traceback.format_exc()))
        return build_response(400, str(e_0))
