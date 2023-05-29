from django.urls import path
from apps.customers.apis.authenticate import generate_otp_api, generate_token_api
from apps.customers.apis.profile.update import basic_info, profile_picture, mobile_number, verify_email
from apps.customers.apis.profile.fetch import fetch_customer_data, otp_for_mobile_no_update, presigned_url_for_dp
from apps.customers.apis.bookings import handle_booking, add_services, fetch_services, fetch_booking, fetch_bookings, request_invoice
from apps.customers.apis.bookings import cancel_booking, calculate_cancellation, fetch_files_uploaded

urlpatterns = [
    
    #OTP
    path(r'generate/otp/', generate_otp_api.index, name="URL to push otp"),

    #Token
    path(r'generate/token/', generate_token_api.index , name="URL to generate token"),
    
    #Fetch
    path(r'profile/fetch/mobilenumber/requestotp/', otp_for_mobile_no_update.index , name="URL to request OTP for mobile Update"),
    path(r'profile/fetch/presigned/url/', presigned_url_for_dp.index , name="URL to get presigned url for file upload"),
    path(r'profile/fetch/info/', fetch_customer_data.index , name="URL to fetch the customer info"),
    
    #Update
    path(r'verify/email/<token>/', verify_email.index , name="URL to verify email"),
    path(r'profile/update/basicinfo/', basic_info.index , name="URL to update the customer basic info"),
    path(r'profile/update/profilepicture/', profile_picture.index , name="URL to fetch the customer info"),
    path(r'profile/update/mobilenumber/', mobile_number.index , name="URL to fetch the customer info"),
    
    #Bookings
    path(r'booking/update/', handle_booking.index, name="URL to add or update booking"),
    path(r'booking/fetch/bookings/', fetch_bookings.index, name="URL to fetch all the bookings of a customer"),
    path(r'booking/fetch/booking/<uuid:booking_id>/', fetch_booking.index, name="URL to fetch the booking info using booking id"),
    path(r'booking/fetch/services/<uuid:booking_id>/', fetch_services.index, name="URL to fetch all the service of a booking"),
    path(r'booking/services/add/', add_services.index, name="URL to add new service(s)"),
    path(r'bookings/fetch/invoice/<uuid:booking_id>/', request_invoice.index, name="URL to fetch the invoice of a booking"),

    #Fetch Files
    path(r'fetchfiles/<uuid:service_id>/', fetch_files_uploaded.index, name="URL to fetch files of a service"),
    
    #Booking Cancellation
    path(r'booking/calculate/cancellation/<uuid:booking_id>/', calculate_cancellation.index, name="URL to calculate the cancellation charges"),
    path(r'booking/cancel/<uuid:booking_id>/', cancel_booking.index, name="URL to cancell a booking completely"),
    
    
]