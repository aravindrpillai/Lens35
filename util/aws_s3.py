import boto3

def get_presigned_url_to_upload_file(bucket_name, file_name):
        url_valid_for = 3 #Seconds
        s3_client = boto3.client('s3')
        s3_response = s3_client.generate_presigned_post(Bucket=bucket_name, Key= file_name, ExpiresIn=url_valid_for)
        return {
            "url" : s3_response['url'],
            "connection_info": s3_response['fields']
        }



def delete_file(bucket_name, file_name):
    s3_client = boto3.client('s3')
    s3_client.delete_object(Bucket=bucket_name, Key=file_name)
    return True
    

def delete_all_from_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    return True

def set_cors_config():
    s3 = boto3.client('s3')
    cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['*'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': ['*'],
            'MaxAgeSeconds': 3000
        }]
    }
    s3.put_bucket_cors(Bucket='my-bucket', CORSConfiguration=cors_configuration)

def create_bucket(bucket_name):
    s3_client = boto3.client('s3')
    if(not check_if_bucket_exist(bucket_name)):
        s3_client.create_bucket(
            Bucket='string',
            CreateBucketConfiguration={ 'LocationConstraint': 'us-east-1' }
        )
    return True

def check_if_bucket_exist(bucket_name):
    s3 = boto3.resource('s3')
    return False if s3.Bucket(bucket_name).creation_date is None else True

def delete_bucket(bucket_name):
    s3_client = boto3.client('s3')
    s3_bucket = s3_client.Bucket(bucket_name)
    s3_bucket.objects.all().delete()
    s3_bucket.delete()