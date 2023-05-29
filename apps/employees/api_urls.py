from django.urls import path
from apps.employees.apis.authenticate import generate_otp_api
from apps.employees.apis.authenticate import generate_token_api
from apps.employees.apis.wallet import fetch_bank_info, update_bank_info 
from apps.employees.apis.profile.fetch import otp_for_mobile_no_update, presigned_url_for_dp_and_idproof, fetch_employee_data
from apps.employees.apis.profile.update import basic_info, services, portfolios, base_location, mobile_number, profile_picture, id_proof, verify_email

from apps.employees.apis.my_bookings import list_my_bookings, services_openfor_update, modify_booking
from apps.employees.apis.open_bookings import accept_booking, list_open_bookings

from apps.employees.apis.file_upload import fetch_done_bookings_with_pending_file_upload, fetch_files_from_service
from apps.employees.apis.file_upload import fetch_booking_info, presigned_url_for_file_upload, acknodwledge_file_upload
from apps.employees.apis.file_upload import delete_file, lock_service

urlpatterns = [

    #OTP
    path(r'generate/otp/', generate_otp_api.index, name="URL to push otp"),

    #Token
    path(r'generate/token/', generate_token_api.index , name="URL to generate token"),

    #Profile Update
    path(r'verify/email/<token>/', verify_email.index , name="URL to verify email"),
    path(r'profile/update/basic/', basic_info.index , name="URL to update basic info"),
    path(r'profile/update/services/', services.index , name="URL to update photographer services"),
    path(r'profile/update/portfolios/', portfolios.index , name="URL to update the portfolios"),
    path(r'profile/update/baselocations/', base_location.index , name="URL to update the base location"),
    path(r'profile/update/mobilenumber/', mobile_number.index , name="URL to update the mobile number"),
    path(r'profile/update/profilepicture/', profile_picture.index , name="URL to update the profile picture"),
    path(r'profile/update/idproof/', id_proof.index , name="URL to update the id proof"),
    
    #Profile Fetch
    path(r'profile/fetch/mobilenumber/requestotp/', otp_for_mobile_no_update.index , name="URL to request OTP for mobile Update"),
    path(r'profile/fetch/presigned/url/', presigned_url_for_dp_and_idproof.index , name="URL to get presigned url for file upload"),
    path(r'profile/fetch/info/', fetch_employee_data.index , name="URL to fetch the employee data"),

    #Wallet
    path(r'wallet/fetch/bank/info/', fetch_bank_info.index , name="URL to fetch the employee bank info"),
    path(r'wallet/update/bank/info/', update_bank_info.index , name="URL to update the employee bank info"),     

    #My Bookings
    path(r'mybookings/list/bookings/', list_my_bookings.index , name="URL to list all bookings which the employee has accepted"),
    path(r'mybookings/list/services/openforupdate/<uuid:booking_id>/', services_openfor_update.index , name="URL to list services open for update"),
    path(r'mybookings/update/booking/', modify_booking.index , name="URL to update the booking"),
    

    #Open Bookings
    path(r'openbookings/list/all/', list_open_bookings.index , name="URL to list all bookings"),
    path(r'openbookings/accept/service/', accept_booking.index , name="URL to accept booking/services"),
    
    #File Upload
    path(r'fileupload/fetch/bookings/<uuid:booking_id>/', fetch_booking_info.index , name="URL to fetch a booking using booking id"),
    path(r'fileupload/fetch/bookings/withpendingfileupload/', fetch_done_bookings_with_pending_file_upload.index , name="URL to fetch bookings of an employee with pending file upload"),
    path(r'fileupload/generate/presignedurl/', presigned_url_for_file_upload.index , name="URL to fetch presigned url for file upload"),
    path(r'fileupload/acknodwledge/', acknodwledge_file_upload.index , name="URL to acknodwledge the file upload"),
    path(r'fileupload/fetch/uploadedfiles/<uuid:service_id>/', fetch_files_from_service.index , name="URL to fetch uploaded files from service"),
    path(r'fileupload/delete/file/', delete_file.index , name="URL to delete file(s) from service"),
    path(r'fileupload/service/lock/<uuid:service_id>/', lock_service.index , name="URL to lock a service"),
]