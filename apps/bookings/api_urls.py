from django.urls import path
from apps.bookings.apis.customers import handle_booking, add_services, remove_services, fetch_services, fetch_bookings, request_invoice
from apps.bookings.apis.employees import list_bookings, fetch_booking_info, accept_booking, remove_booking

urlpatterns = [
    
    #CUSTOMERS - _NOTE_: Start with customers only
    path(r'customers/booking/', handle_booking.index, name="URL to add or update booking"),
    path('customers/bookings/fetch/', fetch_bookings.index, name="URL to fetch all the bookings of a customer"),
    path('customers/services/fetch/<uuid:booking_id>/', fetch_services.index, name="URL to fetch all the service of a booking"),
    path(r'customers/services/add/', add_services.index, name="URL to add new service(s)"),
    path(r'customers/services/remove/', remove_services.index, name="URL to remove service(s)"),
    path(r'customers/fetch/invoice/<uuid:booking_id>/', request_invoice.index, name="URL to fetch the invoice of a booking"),
    
    #EMPLOYEES - _NOTE_: Start with employees only
    path(r'employees/bookings/list/', list_bookings.index , name="URL to list all bookings"),
    path(r'employees/bookings/fetch/<uuid:booking_id>', fetch_booking_info.index , name="URL to fetch a booking using booking id"),
    path(r'employees/bookings/accept/', accept_booking.index , name="URL to accept booking/services"),
    path(r'employees/bookings/remove/', remove_booking.index , name="URL to remove booking/services"),
       
]