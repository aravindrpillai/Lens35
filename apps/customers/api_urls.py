from django.urls import path
from apps.customers.apis.authenticate import generate_otp_api, generate_token_api
from apps.customers.apis.profile.update import basic_info, profile_picture, mobile_number, verify_email
from apps.customers.apis.profile.fetch import fetch_customer_data, otp_for_mobile_no_update, presigned_url_for_dp
 

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
    
    
    
]