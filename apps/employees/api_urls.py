from django.urls import path
from apps.employees.apis import generate_otp_api
from apps.employees.apis import generate_token_api
 

urlpatterns = [
    
    #OTP
    path(r'generate/otp/', generate_otp_api.index, name="URL to push otp"),

    #Token
    path(r'generate/token/', generate_token_api.index , name="URL to generate token"),
    
    
    
       
   
]