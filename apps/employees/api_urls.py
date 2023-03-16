from django.urls import path
from apps.employees.apis.authenticate import generate_otp_api
from apps.employees.apis.authenticate import generate_token_api
from apps.employees.apis.profile.fetch import request_otp_for_mobile_no_update, presigned_url
from apps.employees.apis.profile.update import basic_info, services, portfolios, base_location, mobile_number, profile_picture, id_proof
 

urlpatterns = [
    
    #OTP
    path(r'generate/otp/', generate_otp_api.index, name="URL to push otp"),

    #Token
    path(r'generate/token/', generate_token_api.index , name="URL to generate token"),

    #Profile Update
    path(r'profile/update/basic/', basic_info.index , name="URL to update basic info"),
    path(r'profile/update/services/', services.index , name="URL to update photographer services"),
    path(r'profile/update/portfolios/', portfolios.index , name="URL to update the portfolios"),
    path(r'profile/update/baselocations/', base_location.index , name="URL to update the base location"),
    path(r'profile/update/mobilenumber/', mobile_number.index , name="URL to update the mobile number"),
    path(r'profile/update/profilepicture/', profile_picture.index , name="URL to update the profile picture"),
    path(r'profile/update/idproof/', id_proof.index , name="URL to update the id proof"),
    
    #Profile Fetch
    path(r'profile/fetch/mobilenumber/requestotp/', request_otp_for_mobile_no_update.index , name="URL to request OTP for mobile Update"),
    path(r'profile/fetch/presigned/url/', presigned_url.index , name="URL to get presigned url for file upload"),

    

   
    
    
    
       
   
]