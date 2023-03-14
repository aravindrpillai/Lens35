import os
import base64
from enums.file_types import FILE_TYPES
from serviceapp.settings import MEDIA_URL, MEDIA_ROOT

#file_type should be the enum value
def upload_file(base64_content, file_name_with_extension, file_type_name): 
    try:
        directory = str(FILE_TYPES.get(file_type_name).value)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_full_name = directory+file_name_with_extension
        file_content = base64.urlsafe_b64decode(base64_content)
        with open(file_full_name, 'wb') as f:
            f.write(file_content)
    except Exception as e:
        raise e

#file_type should be the enum value
def delete_file(file_name_with_extension, file_type_name): 
    if(file_name_with_extension == None or file_name_with_extension == ""):
        return 
    try:
        file_full_name = str(FILE_TYPES.get(file_type_name).value)+file_name_with_extension
        os.unlink(file_full_name)
    except Exception as e:
        pass


def get_file_extension(file_type):
    if(file_type == None or file_type == ""):
        raise Exception("File Type cannot be empty")
    match(file_type.lower()):
        case "image/jpeg": return ".jpg"
        case "application/pdf" : return ".pdf" 
        case "image/png" : return ".png"
    raise Exception("Invalid File Type")


def get_full_url_of_file(file_type_name, file_name):
    if(file_name == None or file_name == ""):
        return None
    folder = FILE_TYPES.get(file_type_name).value
    folder_url = folder.replace(MEDIA_ROOT, MEDIA_URL)
    return "{}{}".format(folder_url, file_name)


#For Testing -- Use below code
# with open("C:/aravind/test/a.jpg", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())
#     print(encoded_string)
#     upload_file(encoded_string, "hello.jpg", FILE_TYPES.EMPLOYEE_DP.name)