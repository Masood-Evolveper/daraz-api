from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi import FastAPI, Request, Header, UploadFile, File, Body
import settings
from client import lazop_client, get_access_token, get_all_products, get_auth_code, create_new_product, get_category_attributes, migrate_images, get_migrated_images,migrate_image, get_all_categories, get_category_children, get_category_by_id, get_all_orders, trace_order_by_id, get_product_reviews, get_all_reverse_orders_info, get_order_logistic_details, payout_statement, get_orders_with_items, get_all_products_reviews
from fastapi.responses import RedirectResponse, JSONResponse
from models import DarazProductCreate
from typing import Optional, Any
import os
from dotenv import load_dotenv

_:bool = load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Daraz Backend"}

# https://api.daraz.pk/oauth/authorize?spm=a2o9m.11193531.0.0.97802891wGBXMU&response_type=code&force_auth=true&redirect_uri=https://evolvebitx.netlify.app/callback&client_id=504082
@app.get('/get_auth_code')
async def auth_code():
    auth_url = (
        f"https://api.daraz.pk/oauth/authorize"
        f"?response_type=code&force_auth=true"
        f"&redirect_uri={os.getenv('APP_CALLBACK_URL')}"
        f"&client_id={os.getenv('DARAZ_APP_KEY')}"
    )
    return RedirectResponse(auth_url)

@app.get('/get_access_token')
async def access_token(code: str):
    return get_access_token(code)

@app.get('/get_all_products')
async def all_products(access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_all_products(access_token)

@app.get('/get_all_product_reviews')
async def all_products_reviews(access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_all_products_reviews(access_token)

@app.get('/get_product_reviews')
async def product_reviews(item_id: str, access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_product_reviews(item_id, access_token)

@app.get('/get_all_categories')
async def all_categories():
    return get_all_categories()

@app.get('/get_category_by_id')
async def category_by_id(category_id: int):
    return get_category_by_id(category_id)

@app.get('/get_category_children')
async def category_children(categoty_id: int):
    return get_category_children(categoty_id)

@app.get('/get_category_attributes')
async def category_attributes(category_id: str):
    return get_category_attributes(category_id)

@app.post('/migrate_image')
async def migrate_single_image(image_url: str = Body(..., embed=True), access_token: Optional[str] = Header(None, alias="Authorization")):
    return migrate_image(access_token, image_url)

@app.post('/migrate_images')
async def migrate_all_images(images_urls: list[str], access_token: Optional[str] = Header(None, alias="Authorization")):
    return migrate_images(access_token, images_urls)

@app.get("/migrate_images/result")
async def migrate_images_result(batch_id: str, access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_migrated_images(access_token, batch_id)

@app.post('/create_new_product')
async def new_product(product:dict = Body(...), access_token: Optional[str] = Header(None, alias="Authorization")):
    return create_new_product(access_token, product)

@app.get('/get_all_orders')
async def all_orders(access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_all_orders(access_token)

@app.get('/get_orders_with_items')
async def orders_with_items(access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_orders_with_items(access_token)

@app.get('/trace_order')
async def trace_order(order_id: str, access_token: Optional[str] = Header(None, alias="Authorization")):
    return trace_order_by_id(order_id, access_token)

@app.get('/get_order_logistics_details')
async def order_logistics_details(order_id: str, access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_order_logistic_details(order_id, access_token)

@app.get('/get_all_reverse_orders_info')
async def get_reverse_orders_info(access_token: Optional[str] = Header(None, alias="Authorization")):
    return get_all_reverse_orders_info(access_token)

@app.get('/get_payout')
async def get_payout(access_token: Optional[str] = Header(None, alias="Authorization")):
    return payout_statement(access_token)

# @app.get("/callback")
# async def callback(request: Request):
#     code = request.query_params.get("code")
#     if not code:
#         return JSONResponse({"error": "No code received"})

#     # Exchange code for access token
#     lazop_client = LazopClient("https://api.daraz.pk/rest", APP_KEY, APP_SECRET)
#     lazop_request = LazopRequest("/auth/token/create")
#     lazop_request.add_api_param("code", code)

#     response = lazop_client.execute(lazop_request)

#     return JSONResponse(response.body)



# uvicorn main:app --host 0.0.0.0 --port 8001 --reload