import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Create a S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

# Listar buckets
response = s3.list_buckets()
for bucket in response["Buckets"]:
    print(f"Bucket Name: {bucket['Name']}")

# Escrever em um bucket
bucket_name = os.environ.get("AWS_S3_BUCKT_NAME")
print(bucket_name)

object_name = "agora_foi.txt"
content = "hello, world"
s3.put_object(Bucket=bucket_name, Key=object_name, Body=content)
