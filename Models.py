from pydantic import BaseModel, Field, field_validator, ValidationError,HttpUrl
from typing import Optional
from typing import List
from faker import Faker
from datetime import datetime


class Model(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl

class SupportModel(BaseModel):
    url: HttpUrl
    text: str

class ResponseModel(BaseModel):
    support: SupportModel
    data: Model


class DataModel(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl


class SupportModel(BaseModel):
    url: HttpUrl
    text: str


class ResponseModel(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[DataModel]
    support: SupportModel


class UserRequest(BaseModel):
    name: str
    job: str

    @field_validator('name')
    def validate_name_length(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValidationError('Имя должно быть от 2 до 50 символов')
        return value

    @field_validator('job')
    def validate_job_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValidationError('Название работы должно быть от 2 до 100 символов')
        return value


class UserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: datetime = Field(default_factory=datetime.now)

    @field_validator('name')
    def validate_name_length(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValidationError('Имя должно быть от 2 до 50 символов')
        return value

    @field_validator('job')
    def validate_job_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValidationError('Название работы должно быть от 2 до 100 символов')
        return value

    @field_validator('id')
    def validate_id(cls, value):
        if not value:
            raise ValidationError('ID не может быть пустым')
        return value

    @field_validator('createdAt')
    def validate_created_at(cls, value):
        if not value:
            raise ValidationError('Дата создания не может быть пустой')
        return value


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    job: Optional[str] = None

    @field_validator('name')
    def validate_name(cls, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValidationError('Имя должно быть строкой')
            if len(value) < 2 or len(value) > 50:
                raise ValidationError('Имя должно быть от 2 до 50 символов')
            if not value.replace(' ', '').isalpha():
                raise ValidationError('Имя должно содержать только буквы и пробелы')
        return value

    @field_validator('job')
    def validate_job(cls, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValidationError('Название работы должно быть строкой')
            if len(value) < 2 or len(value) > 100:
                raise ValidationError('Название работы должно быть от 2 до 100 символов')
            if not value.replace(' ', '').isalnum():
                raise ValidationError('Название работы должно содержать только буквы, цифры и пробелы')
        return value

class UpdateUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: datetime = Field(default_factory=datetime.now)

    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValidationError('Имя должно быть от 2 до 50 символов')
        if not value.replace(' ', '').isalpha():
            raise ValidationError('Имя должно содержать только буквы и пробелы')
        return value

    @field_validator('job')
    def validate_job(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValidationError('Название работы должно быть от 2 до 100 символов')
        if not value.replace(' ', '').isalnum():
            raise ValidationError('Название работы должно содержать только буквы, цифры и пробелы')
        return value

    @field_validator('updatedAt')
    def validate_updated_at(cls, value):
        if not isinstance(value, datetime):
            raise ValidationError('Дата обновления должна быть объектом datetime')
        return value

