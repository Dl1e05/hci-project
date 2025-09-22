from fastapi import APIRouter, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.auth.schemas import TokenPair
from app.core.security import decode_token, refresh_tokens

router = APIRouter(prefix="/auth/jwt", tags=["jwt"])

bearer = HTTPBearer(bearerFormat="JWT")


class RefreshInput(BaseModel):
    refresh: str


class VerifyInput(BaseModel):
    token: str


@router.post("/refresh/", response_model=TokenPair, summary="Refresh JWT")
async def jwt_refresh(data: RefreshInput) -> TokenPair:
    return refresh_tokens(data.refresh)


@router.post("/verify/", status_code=status.HTTP_204_NO_CONTENT, summary="Verify JWT")
async def jwt_verify(data: VerifyInput) -> None:
    decode_token(data.token)
    return


@router.get("/authorize/", summary="Authorize with Bearer JWT")
async def jwt_authorize(creds: HTTPAuthorizationCredentials = Security(bearer)) -> dict[str, str]:
    token = creds.credentials
    return {"token": token}