from util.property_reader import PropertyReader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from util.encryption import encrypt
import smtplib

def sent_email_verification_email(to_address, user_name, user_type, user_uuid):
    from_address = PropertyReader.get_property("email", "from_address")
    subject = 'Lens35 email verification'

    with open('static/email_templates/verify_email_template.html', 'r') as html_file:
        html_content = str(html_file.read())
        token_string = encrypt("{}#{}".format(user_uuid, to_address))
        html_content = html_content.replace("__CUSTOMER_NAME__", user_name).replace("__TOKEN__", token_string).replace("__USERTYPE__", user_type)

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    server = smtplib.SMTP(PropertyReader.get_property("email", "smtp"), PropertyReader.get_property("email", "port"))
    server.starttls()
    server.login(PropertyReader.get_property("email", "username"), PropertyReader.get_property("email", "password"))
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

