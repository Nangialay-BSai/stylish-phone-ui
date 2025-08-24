from pydantic import BaseModel, field_validator


class RequestOtp(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("phone required")
        return v


class VerifyOtp(BaseModel):
    phone: str
    code: str


class TokenPair(BaseModel):
    access: str
    refresh: str
