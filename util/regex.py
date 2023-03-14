import re

def validate_and_format_mobile_number(mob_number):
    if(mob_number == None or mob_number == ""):
        raise Exception("Mobile Number is Empty")
    if(re.findall("^[2-9]{1}[0-9]{9}$", mob_number)):
        return mob_number.strip()
    else:
        raise Exception("Invalid Mobile Number")


def validate_and_format_otp(otp):
    if(otp == None or otp == ""):
        raise Exception("OTP is Empty")
    if(re.findall("^[2-9]{1}[0-9]{5}$", otp)):
        return otp.strip()
    else:
        raise Exception("Invalid OTP")

def validate_and_format_uuid4(field_name, uuid_value, supress_error=False):
    if(uuid_value == None or uuid_value == ""):
        if(supress_error):
            return None
        else:
            raise Exception("{} value is empty.".format(field_name))
    try:
        from uuid import UUID
        return UUID(uuid_value, version=4)
    except:
        raise Exception("Device id must be a valid UUID4 (or null)")

def validate_and_format_bool(str_name, str_value):
    if(type(str_value) is bool):
        return str_value
    if(str_value == "" or str_value == None):
        raise Exception("{} is Empty".format(str_name))
    if(str_value == "1" or str_value.lower() == "true"):
        return True
    if(str_value == "0" or str_value.lower() == "false"):
        return False
    raise Exception("value of {} is not boolean.".format(str_name))

def validate_and_format_str(str_name, str_value):
    if(str_value == "" or str_value == None):
        raise Exception("{} is Empty".format(str_name))
    return str_value.strip()

def validate_and_format_email_id(email_id):
    if(email_id == "" or email_id == None):
        raise Exception("Email ID is empty")
    email_id = email_id.strip()
    match = re.search(r'[\w.-]+@[\w.-]+.\w+', email_id)
    if (not match):
        raise Exception("Imvalid Email ID")
    return email_id
