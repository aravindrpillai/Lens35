from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from lens35.settings import BASE_DIR
import os

def send_email(template, template_data, recipient_list, attachments = None):
    
    print("{} -- {} -- {} -- {}".format(template, template_data, recipient_list, attachments))
    subject = 'Subject line of the email'
    from_email = 'emailforlens35@gmail.com'
    
    # Load the HTML and plain text versions of the email message
    template_file = os.path.join(BASE_DIR, 'static', 'email_templates', 'verify_email_template.html')
    print(template_file.replace("\\","/")) 
    html_message = render_to_string(template_file, {'context': 'Your HTML context here'})
    text_message = strip_tags(html_message)

    # Create the email message object and specify the HTML and plain text versions
    msg = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    msg.attach_alternative(html_message, "text/html")

    # Send the email
    msg.send()
