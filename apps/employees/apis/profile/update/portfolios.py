from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from .helper import update_account_status
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        
        portfolios = data.get("portfolios", None)
        if(portfolios != None and portfolios != ""):
            if(len(portfolios) <= 0):
                raise Exception("Portfolios cannot be empty..")    
            employee.portfolios = portfolios
            update_account_status(employee)
            employee.save()
        else:
            raise Exception("Portfolios cannot be empty")

        return build_response(202, "Successfully updated", employee.portfolios)
    except Exception as e_0:
        logger.error('Failed to update employee base location : {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))
