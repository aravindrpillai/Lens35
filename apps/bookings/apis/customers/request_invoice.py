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
        invoice_items = []
        total_amount = 0
        invoices = ServiceInvoice.objects.exclude(service__retired=True).values('service__service').annotate(final_amount_sum=Sum('final_amount'))
        counts = invoices.values('service__service').annotate(count=Count('service__service'))

        # print the counts
        for count in counts:
            total_amount += count['final_amount_sum']
            invoice_items.append({
                "category" : "services",
                "service" : count['service__service'],
                "count" : count['count'],
                "total_cost" : count['final_amount_sum']
            })

        booking_id = UUID(booking_id, version=4)
        already_paid_amount = Transactions.objects.filter(booking__booking_id=booking_id).aggregate(Sum('amount'))['amount__sum']
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
