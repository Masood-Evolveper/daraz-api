from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi import FastAPI, Request
import settings
from client import lazop_client, get_access_token, get_all_products, get_auth_code, create_new_product, get_category_attributes, migrate_images, get_migrated_images, migrate_image
from fastapi.responses import RedirectResponse, JSONResponse
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

# https://api.daraz.pk/oauth/authorize?spm=a2o9m.11193531.0.0.97802891wGBXMU&response_type=code&force_auth=true&redirect_uri=https://evolvebitx.com/callback&client_id=504082
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
async def all_products(access_token: str):
    return get_all_products(access_token)

@app.get('/get_category_attributes')
async def category_attributes(access_token: str, category_id: str):
    return get_category_attributes(access_token, category_id)

@app.post('/migrate_image')
async def migrate_single_image(access_token: str):
    return migrate_image(access_token)

@app.post('/migrate_images')
async def migrate_all_images(access_token: str):
    return migrate_images(access_token)

@app.get("/migrate_images/result")
async def migrate_images_result(access_token: str, batch_id: str):
    return get_migrated_images(access_token, batch_id)

@app.post('/create_new_product')
async def new_product(access_token: str):
    return create_new_product(access_token)

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
