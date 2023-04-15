SMS_OTP_EXPIRY_IN_MINUTES = 2                      # Validity of OTP SMS - Within this time limit the SMS cn can used to login
SMS_RESEND_TIME_LIMIT_IN_MINUTES = 10              # Timelimit to resend OTP SMS - Within 10 minutes, otp resend can be trigged only 3 times 
SMS_OTP_LIMIT_PER_SESSION = 3                      # Maximum no of OTP SMS to be sent in 10 minutes 
TOKEN_EXPIRY_TIME_IN_MINUTES = 10                  # Token validity (if not registered as KEEP_ACTIVE=true)

#EMPLOYEE BUCKET DETAILS
EMPLOYEES_BUCKET = "employees"
EMPLOYEES_DP_FOLDER = "dp"
EMPLOYEES_ID_PROOF_FOLDER = "id_proof"

#CUSTOMER BUCKET DETAILS
CUSTOMERS_BUCKET = "customers"
CUSTOMERS_DP_FOLDER = "dp"

DEFAULT_BOOKING_RANGE_IN_KM = 2

EVENTS = (
    ("wedding" , "Wedding"),
    ("engagement" , "Engagement"),
    ("family" , "Family"),
    ("party" , "Party"),
    ("portrait" , "Portrait"),
    ("maternity" , "Maternity"),
    ("product" , "Product"),
    ("modelling" , "Modelling"),
    ("food" , "Food"),
    ("vehicles" , "Vehicles"),
    ("baby" , "Baby"),
    ("short_film" , "Short Film"),
    ("kids" , "Kids"),
    ("sport" , "Sport"),
    ("pet" , "Pet"),
    ("religious" , "Religious"),
    ("graduation" , "Graduation"),
    ("real_estate" , "Real Estate"),
    ("team_and_office" , "Team and office"),
    ("other" , "Other")
)


SERVICES = (
    ("photography", "photography"),
    ("videography", "videography"),
    ("drone_photography", "drone_photography"),
    ("photo_editing", "photo_editing"), 
    ("video_editing", "video_editing")
)
