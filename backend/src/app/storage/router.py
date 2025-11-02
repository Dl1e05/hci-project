import io
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse

from app.core.storage import StorageService, get_storage_service

router = APIRouter(prefix='/api/v1/storage', tags=['storage'])


def get_storage() -> StorageService:
    """Dependency to get storage service."""
    return get_storage_service()


StorageDep = Annotated[StorageService, Depends(get_storage)]


@router.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Query(default='uploads', description='Folder to upload to'),
    storage: StorageService = Depends(get_storage),
) -> dict:
    try:
        file_key = storage.upload_file(file.file, file.filename or 'unnamed_file', file.content_type, folder)

        metadata = storage.get_file_metadata(file_key)

        return {
            'success': True,
            'file_key': file_key,
            'filename': file.filename,
            'content_type': file.content_type,
            'size': metadata['size'],
            'message': 'File uploaded successfully',
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Upload failed: {str(e)}')


@router.get('/download/{file_key:path}')
async def download_file(file_key: str, storage: StorageService = Depends(get_storage)) -> StreamingResponse:
    try:
        if not storage.file_exists(file_key):
            raise HTTPException(status_code=404, detail='File not found')

        file_content = storage.download_file(file_key)
        metadata = storage.get_file_metadata(file_key)

        return StreamingResponse(
            io.BytesIO(file_content),
            media_type=metadata.get('content_type', 'application/octet-stream'),
            headers={'Content-Disposition': f'attachment; filename="{file_key.split("/")[-1]}"'},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Download failed: {str(e)}')


@router.delete('/delete/{file_key:path}')
async def delete_file(file_key: str, storage: StorageService = Depends(get_storage)) -> dict:
    try:
        if not storage.file_exists(file_key):
            raise HTTPException(status_code=404, detail='File not found')

        storage.delete_file(file_key)

        return {'success': True, 'file_key': file_key, 'message': 'File deleted successfully'}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Deletion failed: {str(e)}')


@router.get('/list')
async def list_files(
    prefix: str = Query(default='', description='Folder prefix to filter by'),
    max_keys: int = Query(default=100, ge=1, le=1000, description='Maximum number of files to return'),
    storage: StorageService = Depends(get_storage),
) -> dict:
    try:
        files = storage.list_files(prefix=prefix, max_keys=max_keys)

        return {'success': True, 'count': len(files), 'files': files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to list files: {str(e)}')


@router.get('/url/{file_key:path}')
async def get_presigned_url(
    file_key: str,
    expiration: int = Query(default=3600, ge=60, le=86400, description='URL expiration in seconds'),
    storage: StorageService = Depends(get_storage),
) -> dict:
    try:
        if not storage.file_exists(file_key):
            raise HTTPException(status_code=404, detail='File not found')

        url = storage.generate_presigned_url(file_key, expiration)

        return {'success': True, 'file_key': file_key, 'url': url, 'expires_in': expiration}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to generate URL: {str(e)}')
