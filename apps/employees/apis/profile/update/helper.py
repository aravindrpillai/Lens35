def update_account_status(employee):
    unfilled_fileds = get_unfilled_fileds(employee)
    employee.is_draft = len(unfilled_fileds) > 1
    

def get_unfilled_fileds(employee):

    unfilled_fields = []

    if(employee.full_name == None):
        unfilled_fields.append("full_name")

    if(employee.profile_name == None):
        unfilled_fields.append("profile_name")

    if(employee.email_id == None):
        unfilled_fields.append("email_id")
    
    
    if(employee.id_proof_type == None):
        unfilled_fields.append("id_proof_type")

    if(employee.id_proof_front == None):
        unfilled_fields.append("id_proof_front")

    if(employee.id_proof_back == None):
        unfilled_fields.append("id_proof_back")
    
    if(employee.base_location_pincode == None):
        unfilled_fields.append("base_location_pincode")

    if(employee.base_location_city == None):
        unfilled_fields.append("base_location_city")
    
    if(employee.portfolios == None or len(employee.portfolios) < 1):
        unfilled_fields.append("portfolios")

    if(employee.is_photographer == False and
        employee.is_videographer == False and 
        employee.is_drone_photographer == False and
        employee.is_photo_editor == False and 
        employee.is_video_editor == False):
        unfilled_fields.append("services")

    return unfilled_fields