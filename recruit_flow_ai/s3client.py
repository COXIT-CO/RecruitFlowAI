"""
S3StorageManager

This module provides a class for managing storage on S3-compatible services
like Minio. The S3StorageManager class uses the Minio Python SDK to interact
with the storage service.

The MinioSettings class is a Pydantic model that loads Minio configuration
from environment variables.

The S3StorageManager class provides methods for uploading files, checking
if a bucket exists, and setting the bucket policy. It logs errors and other
important events.

Environment Variables:
- MINIO_ENDPOINT: The URL of the Minio service.
- MINIO_ACCESS_KEY: The access key for the Minio service.
- MINIO_SECRET_KEY: The secret key for the Minio service.

Minio should be configured to make links publicly accessable
mc alias set myminio https://your_minioapi_domain.com usrname password
mc anonymous set public myminio/bucket_name

Classes:
- MinioSettings: A Pydantic model for Minio configuration.
- S3StorageManager: A class for managing storage on S3-compatible services.

Exceptions:
- ValidationError: Raised when there is an error in the Minio settings.
"""
import logging
import os
from io import BytesIO
from minio import Minio
from pydantic import SecretStr
from pydantic_settings import BaseSettings

class MinioSettings(BaseSettings):
    endpoint: str
    access_key: SecretStr
    secret_key: SecretStr
    bucket: str

    class Config:
        env_prefix = "MINIO_"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3StorageManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        try:
            self.minio_settings = MinioSettings()
            self.client = Minio(
                endpoint=self.minio_settings.endpoint,
                access_key=self.minio_settings.access_key.get_secret_value(),
                secret_key=self.minio_settings.secret_key.get_secret_value(),
                secure=False
            )

            if not self.client.bucket_exists(self.minio_settings.bucket):
                raise ValueError(f"Bucket {self.minio_settings.bucket} does not exist.")

            self.check_and_set_bucket_policy(self.minio_settings.bucket)
        except Exception as e:
            logging.error(f"Error initializing S3StorageManager: {e}")
            raise e

    def upload_pdf(self, pdf_file_path):
        try:
            with open(pdf_file_path, 'rb') as f:
                data = BytesIO(f.read())
                length = data.getbuffer().nbytes
                object_name = os.path.basename(pdf_file_path)
                self.client.put_object(bucket_name=self.minio_settings.bucket,
                                             object_name=object_name, 
                                             data=data, 
                                             length=length,
                                             content_type='application/pdf')
            logging.info(f"Uploaded {object_name} to {self.minio_settings.bucket}")
            return f"https://{self.minio_settings.endpoint}/{self.minio_settings.bucket}/{object_name}"
        except Exception as e:
            logging.error(f"Error uploading to Minio: {e}")

    def bucket_exists(self, bucket_name):
        return self.client.bucket_exists(bucket_name)
        
    def check_and_set_bucket_policy(self, bucket_name):
        try:
            policy = self.minio_client.get_bucket_policy(bucket_name)
            logging.info(f"Current policy: {policy}")
            
            if policy != 'READ_WRITE':
                self.minio_client.set_bucket_policy(bucket_name, 'READ_WRITE')
                logging.warn("Bucket policy set to 'READ_WRITE'")
        except Exception as e:
            logging.error(f"Error setting bucket policy: {e}")

 