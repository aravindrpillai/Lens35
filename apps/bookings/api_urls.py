from django.urls import path
from apps.bookings.apis.customers import handle_booking, add_services, fetch_services, fetch_booking, fetch_bookings, request_invoice
from apps.bookings.apis.customers import cancel_booking, calculate_cancellation, fetch_files_uploaded
from apps.bookings.apis.employees.my_bookings import list_my_bookings ,remove_booking
from apps.bookings.apis.employees.open_bookings import accept_booking, list_open_bookings
from apps.bookings.apis.employees.file_upload import fetch_done_bookings_with_pending_file_upload, fetch_files_from_service
from apps.bookings.apis.employees.file_upload import fetch_booking_info, presigned_url_for_file_upload, acknodwledge_file_upload
from apps.bookings.apis.employees.file_upload import delete_file, lock_service

urlpatterns = [
    
    #CUSTOMERS - _NOTE_: Start the url with customers only
    path(r'customers/booking/', handle_booking.index, name="URL to add or update booking"),
    path(r'customers/bookings/fetch/', fetch_bookings.index, name="URL to fetch all the bookings of a customer"),
    path(r'customers/booking/fetch/<uuid:booking_id>/', fetch_booking.index, name="URL to fetch the booking info using booking id"),
    path(r'customers/services/fetch/files/<uuid:service_id>/', fetch_files_uploaded.index, name="URL to fetch files of a service"),
    path(r'customers/services/fetch/<uuid:booking_id>/', fetch_services.index, name="URL to fetch all the service of a booking"),
    path(r'customers/services/add/', add_services.index, name="URL to add new service(s)"),
    path(r'customers/fetch/invoice/<uuid:booking_id>/', request_invoice.index, name="URL to fetch the invoice of a booking"),
    path(r'customers/calculate/cancellation/<uuid:booking_id>/', calculate_cancellation.index, name="URL to calculate the cancellation charges"),
    path(r'customers/cancel/booking/<uuid:booking_id>/', cancel_booking.index, name="URL to cancell a booking completely"),

    
    
    #EMPLOYEES - _NOTE_: Start the url with employees only
    path(r'employees/open/bookings/', list_open_bookings.index , name="URL to list all bookings"),
    path(r'employees/my/bookings/', list_my_bookings.index , name="URL to list all bookings which the employee has accepted"),
    path(r'employees/bookings/fetch/<uuid:booking_id>/', fetch_booking_info.index , name="URL to fetch a booking using booking id"),
    path(r'employees/fetch/bookings/withpendingfileupload/', fetch_done_bookings_with_pending_file_upload.index , name="URL to fetch bookings of an employee with pending file upload"),
    path(r'employees/bookings/accept/', accept_booking.index , name="URL to accept booking/services"),
    path(r'employees/bookings/remove/', remove_booking.index , name="URL to remove booking/services"),
    path(r'employees/bookings/fileupload/fetch/presignedurl/', presigned_url_for_file_upload.index , name="URL to fetch presigned url for file upload"),
    path(r'employees/bookings/fileupload/acknodwledge/', acknodwledge_file_upload.index , name="URL to acknodwledge the file upload"),
    path(r'employees/bookings/fetch/uploadedfiles/<uuid:service_id>/', fetch_files_from_service.index , name="URL to fetch uploaded files from service"),
    path(r'employees/bookings/file/delete/', delete_file.index , name="URL to delete file(s) from service"),
    path(r'employees/bookings/services/lock/<uuid:service_id>/', lock_service.index , name="URL to lock a service"),
       
]