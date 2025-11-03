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


