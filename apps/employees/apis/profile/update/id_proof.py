from util.wasabi import delete_file_from_bucket, get_presigned_url_to_access_object
from lens35.constanst import EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER
from apps.employees.models.employees import Employees
from rest_framework.decorators import api_view
from util.http import build_response
from util.logger import logger
import traceback

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        employee = Employees.objects.get(employee_id = employee_id)
        data = request.data
        
        document_type = __validate_and_format_document_type(data.get("document_type", None))
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
        employee.save()
        response = {
            "front_link": get_presigned_url_to_access_object(EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER, front_file_name),
            "back_link": get_presigned_url_to_access_object(EMPLOYEES_BUCKET, EMPLOYEES_ID_PROOF_FOLDER, back_file_name)
        }
        return build_response(202, "ID Proof updated successfully", response)
        
    except Exception as e_0:
        logger.error('Failed to update ID Proof for employee {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))
    

def __validate_and_format_document_type(document_type):
    # 'A'- 'Aadhar' || 'P', 'Passport'  || 'D', 'DrivingLicence'  || 'V', 'VotersID'
    if(document_type == None or document_type == ""):
        raise Exception("Document Type cannot be empty.")
    document_type = document_type.lower()
    match document_type:
        case "aadhar":
            return "A"
        case "passport":
            return "P"
        case "driving_licence":
            return "D"
        case "voters_id":
            return "V"
        case __:
            raise Exception("Invalid Document Type")