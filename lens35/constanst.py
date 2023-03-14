SMS_OTP_EXPIRY_IN_MINUTES = 2                      # Validity of OTP SMS - Within this time limit the SMS cn can used to login
SMS_RESEND_TIME_LIMIT_IN_MINUTES = 10              # Timelimit to resend OTP SMS - Within 10 minutes, otp resend can be trigged only 3 times 
SMS_OTP_LIMIT_PER_SESSION = 3                      # Maximum no of OTP SMS to be sent in 10 minutes 
TOKEN_EXPIRY_TIME_IN_MINUTES = 10                  # Token validity (if not registered as KEEP_ACTIVE=true)