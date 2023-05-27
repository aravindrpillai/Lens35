from util.wasabi import delete_file_from_bucket
from rest_framework.decorators import api_view
from lens35.constanst import BOOKINGS_BUCKET
from apps.bookings.models.files import Files
from util.http import build_response
from util.logger import logger
import traceback
import uuid

@api_view(['POST'])
def index(request):
    try:
        employee_id = request.headers.get("Identifier")
        data = request.data
        file_ids = data.get("file_ids", [])

        file_uuids = [uuid.UUID(file_id) for file_id in file_ids]
        files = Files.objects.filter(file_id__in=file_uuids, service__employee__employee_id=employee_id)
        not_found_file_ids = list(set(file_uuids) - set(files.values_list('file_id', flat=True)))
        if(not_found_file_ids):
            raise Exception("File with id {} cannot be found".format(not_found_file_ids))    
        for file in files:
            file_name_in_repo = str(file.file_id)+"."+file.file_name.split(".")[1]
            delete_file_from_bucket(BOOKINGS_BUCKET, file.service.service_id, file_name_in_repo)
            file.delete()
        return build_response(200, None, "Success")
    except Exception as e_0:
        logger.error('Failed to delete file(s) : Employee id {} - {}\n{}'.format(employee_id, e_0, traceback.format_exc()))
        return build_response(400, str(e_0))