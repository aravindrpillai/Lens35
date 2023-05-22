CANCELLATION_CHARGE = 200
PHOTOGRAPHER_RATE_PER_HOUR = 1000
VIDEOGRAPHER_RATE_PER_HOUR = 1200
DRONE_RATE_PER_HOUR = 1500
CURRENT_TAX_PERCENTAGE = 12

SMS_OTP_EXPIRY_IN_MINUTES = 2                      # Validity of OTP SMS - Within this time limit the SMS cn can used to login
SMS_RESEND_TIME_LIMIT_IN_MINUTES = 10              # Timelimit to resend OTP SMS - Within 10 minutes, otp resend can be trigged only 3 times 
SMS_OTP_LIMIT_PER_SESSION = 3                      # Maximum no of OTP SMS to be sent in 10 minutes 
TOKEN_EXPIRY_TIME_IN_MINUTES = 10                  # Token validity (if not registered as KEEP_ACTIVE=true)

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


SERVICES = (
    ("photography", "photography"),
    ("videography", "videography"),
    ("drone_photography", "drone_photography"),
    ("photo_editing", "photo_editing"), 
    ("video_editing", "video_editing")
)

COST_CATEGORIES = (
    ("booking_cost", "booking_cost"),
    ("cancellation_charge", "cancellation_charge"),
    ("discount", "discount")
)
