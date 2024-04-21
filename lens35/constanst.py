CANCELLATION_CHARGE = 200
EMPLOYEE_SERVICE_CANCELLATION_CHARGE = 200
PHOTOGRAPHER_RATE_PER_HOUR = 1000
VIDEOGRAPHER_RATE_PER_HOUR = 1200
DRONE_RATE_PER_HOUR = 1500
CURRENT_TAX_PERCENTAGE = 12

SMS_OTP_EXPIRY_IN_MINUTES = 2                      # Validity of OTP SMS - Within this time limit the SMS cn can used to login
SMS_RESEND_TIME_LIMIT_IN_MINUTES = 5              # Timelimit to resend OTP SMS - Within 10 minutes, otp resend can be trigged only 3 times 
SMS_OTP_LIMIT_PER_SESSION = 3                      # Maximum no of OTP SMS to be sent in 10 minutes 
TOKEN_EXPIRY_TIME_IN_MINUTES = 10                  # Token validity (if not registered as KEEP_ACTIVE=true)

#Booking cannot be added or modified if CurrentDateTime - BookingDateTime < this duration  
BOOKING_BUFFER = 12 #in hours

#EMPLOYEE BUCKET DETAILS
EMPLOYEES_BUCKET = "lens35-employees-001"
EMPLOYEES_DP_FOLDER = "dp"
EMPLOYEES_ID_PROOF_FOLDER = "id_proof"

#BOOKINGS BUCKET
BOOKINGS_BUCKET = "lens35-bookings-001"

#CUSTOMER BUCKET DETAILS
CUSTOMERS_BUCKET = "lens35-customers-001"
CUSTOMERS_DP_FOLDER = "dp"

DEFAULT_BOOKING_RANGE_IN_KM = 2

EVENTS = (
    ("wedding" , "Wedding"),
    ("engagement" , "Engagement"),
    ("family" , "Family"),
    ("party" , "Party"),
    ("portrait" , "Portrait"),
    ("event" , "Event"),
    ("maternity" , "Maternity"),
    ("real_estate" , "Real Estate"),
    ("graduation" , "Graduation"),
    ("team_and_office" , "Team and office"),
    ("product" , "Product"),
    ("modelling" , "Modelling"),
    ("food" , "Food"),
    ("vehicles" , "Vehicles"),
    ("baby" , "Baby"),
    ("kids" , "Kids"),
    ("sport" , "Sport"),
    ("pet" , "Pet"),
    ("religious" , "Religious"),
    ("short_film" , "Short Film"),
    ("other" , "Other")
)


#Use the below variables for services in code
PHOTOGRAPHY = "photography"
VIDEOGRAPHY = "videography"
DRONE = "drone"
PHOTO_EDITING = "photo_editing"
VIDEO_EDITING = "video_editing"

#Choice for table Services.service
SERVICES = (
    (PHOTOGRAPHY, PHOTOGRAPHY),
    (VIDEOGRAPHY, VIDEOGRAPHY),
    (DRONE, DRONE),
    (PHOTO_EDITING, PHOTO_EDITING), 
    (VIDEO_EDITING, VIDEO_EDITING)
)


#use the below for cost categories in code
BOOKING_COST = "booking_cost"
CANCELLATION_CHARGE = "cancellation_charge"
DISCOUNT = "discount"

#Choice for Cost categories
COST_CATEGORIES = (
    (BOOKING_COST, BOOKING_COST),
    (CANCELLATION_CHARGE, CANCELLATION_CHARGE),
    (DISCOUNT, DISCOUNT)
)