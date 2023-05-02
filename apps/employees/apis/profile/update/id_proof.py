from util.wasabi import delete_file_from_bucket, get_presigned_url_to_access_object
from lens35.constanst import EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER
from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.http import build_response
from .helper import update_account_status
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data

        document_type = data.get("document_type", None)
        valid_document_types = ['aadharcard', 'passport', 'driving_licence', 'voters_id']
        if((document_type == None or document_type == "") or (not (document_type.lower() in valid_document_types))):
            raise Exception("Document Type cannot be empty. Value must be one amongst {}".format(str(valid_document_types)))
        document_type = document_type.lower()    
        front_file_name = data.get("front_file_name", None)
        back_file_name = data.get("back_file_name", None)
        if(front_file_name == None or back_file_name == None or front_file_name == "" or back_file_name == ""):
            raise Exception("ID Proof cannot be empty")
        
        try:
            if(employee.id_proof_front != None):
                delete_file_from_bucket(EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER, employee.id_proof_front)
            if(employee.id_proof_back != None):
                delete_file_from_bucket(EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER, employee.id_proof_back)
        except Exception as e_1:
            #Supressing the error - because orphaned filed will be handled by a separate lambda function
            logger.error('Failed to delete the old ID Proof of employee {} - {}\n{}'.format(employee_id, e_1, traceback.format_exc()))

        employee.id_proof_type = document_type
        employee.id_proof_front = front_file_name
        employee.id_proof_back = back_file_name

        update_account_status(employee)
        employee.save()
        response = {
            "front_link": get_presigned_url_to_access_object(EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER, front_file_name),
            "back_link": get_presigned_url_to_access_object(EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER, back_file_name)
        }
        return build_response(201, "ID Proof updated successfully", response)
        
    except Exception as e_0:
        logger.error('Failed to update ID Proof for employee {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))
