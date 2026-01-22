import boto3
import os

session = boto3.session.Session()

s3 = session.client(
    service_name="s3",
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
    region_name="auto",
)

BUCKET = os.getenv("R2_BUCKET")
PUBLIC_URL = os.getenv("R2_PUBLIC_URL")
