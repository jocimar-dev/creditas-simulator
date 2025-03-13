from pydantic import BaseModel, EmailStr

class ContactRequest(BaseModel):
    address: str
    phone: str
    email: EmailStr
