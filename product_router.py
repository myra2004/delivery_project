
from fastapi import APIRouter
from fastapi_jwt_auth import AuthJWT
from models import User, Product
from schemas import ProductModel
from database import session, engine
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

product_router = APIRouter(
    prefix='/product'
)

session = session(bind=engine)

@product_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel, Authorize: AuthJWT = Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        new_product = ProductModel(
            name= product.name,
            price = product.price,
        )
        session.add(new_product)
        session.commit()
        data = {
            'success': True,
            'code': 201,
            'message': 'Product created successfully',
            'data': {
                'id': new_product.id,
                'name': new_product.name,
                'price': new_product.price,
            }
        }
        return jsonable_encoder(data)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admin can add a new product')


@product_router.get('/list', status_code=status.HTTP_200_OK)
async def list_all_products(Authoriza: AuthJWT=Depends()):
    # barcha mahsulatlar ro`yxatini chiqarish uchun funksiya

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")


    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username==user).first()
    if current_user.is_staff:
        products = session.query(Product).all()
        custom_data = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price
            }
            for product in products
        ]

        return jsonable_encoder(custom_data)

    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admin can see all products')


@product_router.get('/{id}/delete')
async def get_product_by_id(id: int, Authorize: AuthJWT = Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            custom_order= [
                {
                    'id': product.id,
                    'product_id': product.product_id,
                    'price': product.price
                }
            ]
            return jsonable_encoder(custom_order)

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Super Admin can get the request")


@product_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            session.delete(product)
            session.commit()
            data= {
                'success': True,
                'code': 200,
                'message': f'Product with id {id} deleted successfully',
                'data': None
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only Super Admin can delete the product'
        )


@product_router.put('/{id}/update', status_code=status.HTTP_200_OK)
async def update_product_by_id(id: int, update_data: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(product, key, value)
            session.commit()
            data = {
                'success': True,
                'code': 200,
                'message': f'Product with id {id} updated successfully',
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price
                }
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only Super Admin can delete the product'
        )

