from pydantic import BaseModel
from typing import Optional



class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]



    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'mohirdev',
                'email': 'mohirdev@gmail.com',
                'password': '12345',
                'is_staff': False,
                'is_active': True
            }
        }



class Settings(BaseModel):
    authjwt_secret_key: str = '63fc2915cff040d17fe6c0d3ed65f6d0d0dbf2eb5bd785835453b16a452d0d8f'


class LoginModel(BaseModel):
    username_or_email: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_statuses: Optional[str] = "PENDING"
    user_id: Optional[int]
    product_id: int

    class Config:
        orm_mode=True
        schema_extra={
            'example': {
                'quantity': 2,
            }
        }


class OrderStatusModel(BaseModel):
    order_statuses: Optional[str] = "PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            'example': {
                'order_statuses': "PENDING",
            }
        }


class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    price: int

    class Config:
        orm_mode=True
        schema_extra={
            'example': {
                'name': "Uzbek plov",
                'price': 50000
            }
        }