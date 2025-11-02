import os
from typing import BinaryIO

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

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


class StorageService:
    """Service for handling file storage operations with Cloudflare R2."""

    def __init__(self) -> None:
        """Initialize the S3 client for Cloudflare R2."""
        self.bucket_name = R2_BUCKET_NAME

        self.s3_client = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
            region_name='auto',  # R2 uses 'auto' for region
        )

    def upload_file(self, file: BinaryIO, file_name: str, content_type: str | None = None, folder: str = '') -> str:
        """
        Upload a file to R2 bucket.

        Args:
            file: File object to upload
            file_name: Name of the file in the bucket
            content_type: MIME type of the file
            folder: Optional folder path in the bucket

        Returns:
            str: The key (path) of the uploaded file in the bucket

        Raises:
            ClientError: If upload fails
        """
        # Construct the full key with folder path
        key = f'{folder}/{file_name}'.strip('/') if folder else file_name

        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type

        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, key, ExtraArgs=extra_args)
            return key
        except ClientError as e:
            raise RuntimeError(f'Failed to upload file: {e}')

    def download_file(self, key: str) -> bytes:
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read()
        except ClientError as e:
            raise RuntimeError(f'Failed to download file: {e}')

    def delete_file(self, key: str) -> None:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            raise RuntimeError(f'Failed to delete file: {e}')

    def file_exists(self, key: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def generate_presigned_url(self, key: str, expiration: int = 3600, http_method: str = 'GET') -> str:
        try:
            client_method = 'get_object' if http_method == 'GET' else 'put_object'
            url = self.s3_client.generate_presigned_url(
                client_method, Params={'Bucket': self.bucket_name, 'Key': key}, ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise RuntimeError(f'Failed to generate presigned URL: {e}')

    def list_files(self, prefix: str = '', max_keys: int = 1000) -> list[dict]:
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, MaxKeys=max_keys)

            if 'Contents' not in response:
                return []

            return [
                {'key': obj['Key'], 'size': obj['Size'], 'last_modified': obj['LastModified'], 'etag': obj['ETag']}
                for obj in response['Contents']
            ]
        except ClientError as e:
            raise RuntimeError(f'Failed to list files: {e}')

    def get_file_metadata(self, key: str) -> dict:
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return {
                'key': key,
                'size': response['ContentLength'],
                'content_type': response.get('ContentType'),
                'last_modified': response['LastModified'],
                'etag': response['ETag'],
            }
        except ClientError as e:
            raise RuntimeError(f'Failed to get file metadata: {e}')


_storage_service: StorageService | None = None


def get_storage_service() -> StorageService:
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service
