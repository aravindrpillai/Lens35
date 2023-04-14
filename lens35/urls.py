from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'employees/apis/', include("apps.employees.api_urls")),
    path(r'customers/apis/', include("apps.customers.api_urls")),
    
    
    path(r'bookings/apis/', include("apps.bookings.api_urls")),   

]
