import os
from typing import BinaryIO

import boto3
import urllib3
from botocore.config import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# Disable SSL warnings for development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME', 'hci-project')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL', f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com')

DEBUG = os.getenv('DEBUG', 'False') == 'True'
APP_NAME = 'Cloudflare R2 Storage API'
APP_VERSION = '1.0.0'

if not all([R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID]):
    raise ValueError(
        'Missing required R2 configuration. Please set R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, and R2_ACCOUNT_ID in .env'
    )

R2_PUBLIC_URL: str = os.getenv('R2_PUBLIC_URL', f'https://pub-{R2_ACCOUNT_ID}.r2.dev')


class StorageService:
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
            verify=False,
        )
        self.bucket_name = R2_BUCKET_NAME

    def upload_file(self, file_obj: BinaryIO, filename: str, content_type: str | None = None, folder: str = 'uploads') -> str:
        import uuid

        file_extension = os.path.splitext(filename)[1]
        unique_filename = f'{uuid.uuid4()}{file_extension}'
        file_key = f'{folder}/{unique_filename}'

        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type

        self.s3_client.upload_fileobj(file_obj, self.bucket_name, file_key, ExtraArgs=extra_args)

        return file_key

    def download_file(self, file_key: str) -> bytes:
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
        return response['Body'].read()

    def delete_file(self, file_key: str) -> None:
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)

    def file_exists(self, file_key: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except ClientError:
            return False

    def get_file_metadata(self, file_key: str) -> dict:
        response = self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
        return {
            'size': response['ContentLength'],
            'content_type': response.get('ContentType', 'application/octet-stream'),
            'last_modified': response['LastModified'],
        }

    def list_files(self, prefix: str = '', max_keys: int = 100) -> list[dict]:
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, MaxKeys=max_keys)

        files = []
        for obj in response.get('Contents', []):
            files.append(
                {
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                }
            )
        return files

    def generate_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        return self.s3_client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket_name, 'Key': file_key}, ExpiresIn=expiration
        )

    def get_public_url(self, file_key: str) -> str:
        file_key = file_key.lstrip('/')
        base_url = R2_PUBLIC_URL.rstrip('/')
        return f'{base_url}/{file_key}'


_storage_service: StorageService | None = None


def get_storage_service() -> StorageService:
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service
