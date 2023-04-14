from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback
from util.email_util import send_email


@api_view(['GET'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        print("EMp id  : {}".format(employee_id))
        employee = Employees.objects.get(employee_id = employee_id)
        

        template = "verify_email_template"
        template_data = {}
        recipient_list = ["aravind.ramachandran.pillai@gmail.com"] 
        attachments = None
        send_email(template, template_data, recipient_list, attachments)

        return build_response(200, "Success")
    except Exception as e_0:
        logger.error('Failed to fetch Employee information : {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))