from pydantic import BaseModel, Field, field_validator

# Simple, dependency-free email check (something@something.tld)
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=254, pattern=EMAIL_PATTERN)
    password: str = Field(min_length=8, max_length=72)  # bcrypt uses max 72 bytes

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        # Trim spaces and lowercase before the format check runs
        return value.strip().lower() if isinstance(value, str) else value


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254, pattern=EMAIL_PATTERN)
    password: str = Field(min_length=1, max_length=72)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        # Trim spaces and lowercase before the format check runs
        return value.strip().lower() if isinstance(value, str) else value
