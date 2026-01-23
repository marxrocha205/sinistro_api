import boto3
from app.core.config import settings

session = boto3.session.Session()

s3 = session.client(
    service_name="s3",
    endpoint_url=settings.r2_endpoint,
    aws_access_key_id=settings.r2_access_key,
    aws_secret_access_key=settings.r2_secret_key,
    region_name="auto",
)

BUCKET = settings.r2_bucket
PUBLIC_URL = settings.r2_public_url
