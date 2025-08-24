from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.user import User, UserRole
from ..schemas.auth import RequestOtp, VerifyOtp, TokenPair
from ..services import otp as otp_service
from ..core.security import create_access_token, create_refresh_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/request-otp")
async def request_otp(payload: RequestOtp):
    code = otp_service.generate_and_store_otp(payload.phone)
    # TODO: integrate SMS/WhatsApp provider. For now, return masked.
    return {"sent": True, "to": payload.phone[-4:], "hint": code[-2:]}


@router.post("/verify-otp", response_model=TokenPair)
async def verify_otp(payload: VerifyOtp, db: Session = Depends(get_db)):
    if not otp_service.verify_otp(payload.phone, payload.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")

    user = db.query(User).filter(User.phone == payload.phone).one_or_none()
    if user is None:
        user = User(phone=payload.phone, role=UserRole.rider)
        db.add(user)
        db.commit()
        db.refresh(user)

    access = create_access_token(sub=str(user.id), extra={"role": user.role})
    refresh = create_refresh_token(sub=str(user.id))
    return TokenPair(access=access, refresh=refresh)
