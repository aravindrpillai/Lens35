from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(template, template_data, recipient_list, attachments = None):
    # subject = "Derive based on template"
    # if recipient_list == None:
    #     raise Exception("No Recipient Found")
    # template = 'email_templates/'+template
    # message = render_to_string(template, template_data)
    # msg = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, recipient_list)

    # if attachments != None:
    #     for attachment in attachments:
    #         msg.attach_file(attachment)

    # msg.attach_alternative(message, "text/html")
    # msg.send()
    pass