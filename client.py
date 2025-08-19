from python.lazop.base import LazopClient, LazopRequest
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import json
from models import DarazProductCreate

_:bool = load_dotenv()

lazop_client = LazopClient("https://api.daraz.pk/rest", os.getenv("DARAZ_APP_KEY"), os.getenv("DARAZ_APP_SECRET"))

def get_auth_code():
    pass

def get_access_token(code: str):
    access_token_request = LazopRequest("/auth/token/create")
    access_token_request.add_api_param("code", code)
    access_token_response = lazop_client.execute(access_token_request)
    print("Auth access token: ", access_token_response.body)
    access_token = access_token_response.body["access_token"]
    return access_token

def get_all_products(access_token: str):
    all_products_request = LazopRequest("/products/get",'GET')
    all_products_request.add_api_param("offset", "0")
    all_products_request.add_api_param("limit", "10")
    all_products_request.add_api_param('filter', 'live')
    all_products_response = lazop_client.execute(all_products_request, access_token)
    print("Products: ", all_products_response.body)
    return all_products_response.body

            #   <delivery_option_sof>Yes</delivery_option_sof>

def get_category_attributes(access_token: str, category_id: str):
    request = LazopRequest("/category/attributes/get", "GET")
    request.add_api_param("primary_category_id", category_id)
    response = lazop_client.execute(request, access_token)
    return response.body

def get_all_categories(access_token: str):
    request = LazopRequest("/category/tree/get", "GET")
    response = lazop_client.execute(request, access_token)
    return response.body

def get_category_children(access_token: str, category_id: int):
    all_categories_request = LazopRequest("/category/tree/get", "GET")
    response = lazop_client.execute(all_categories_request, access_token)

    import json
    all_categories_tree = response.body
    if isinstance(all_categories_tree, str):
        all_categories_tree = json.loads(all_categories_tree)

    categories = all_categories_tree.get("data", [])

    def find_category(categories, category_id):
        for category in categories:
            # FIX: Daraz uses "category_id", not "id"
            if int(category["category_id"]) == category_id:
                return category.get("children", [])
            children = category.get("children", [])
            if children:
                found = find_category(children, category_id)
                if found is not None:
                    return found
        return None

    return find_category(categories, category_id) or []

def migrate_image(access_token: str):
  request = LazopRequest('/image/migrate')
  xml_payload = """
<Request>
    <Image>
        <Url>https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_t.png</Url>
    </Image>
</Request>
  """
  request.add_api_param("payload", xml_payload)
  response = lazop_client.execute(request, access_token)
  print(response)
  if isinstance(response.body, dict):
        return response.body
  else:
    return json.loads(response.body)
  
def migrate_images(access_token: str):
  image_urls = [
    "https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_t.png",
    "https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_t.png"
    ]
  request = LazopRequest('/images/migrate')
  
  xml_payload = """
  <?xml version="1.0" encoding="UTF-8" ?>
<Request>
    <Images>
        <Url>https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_t.png</Url>
        <Url>https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_t.png</Url>
    </Images>
</Request>
  """
  request.add_api_param("payload", xml_payload)
  response = lazop_client.execute(request, access_token)
  print(response)
  if isinstance(response.body, dict):
        return response.body
  else:
    return json.loads(response.body)
  
def get_migrated_images(access_token: str, batch_id: str):
    request = LazopRequest('/image/response/get', 'GET')
    request.add_api_param('batch_id', batch_id)
    response = lazop_client.execute(request, access_token)
    print(response)
    if isinstance(response.body, dict):
        return response.body
    return json.loads(response.body)
  
    #  <Image>https://static-01.daraz.pk/p/97545b9b42e3a4781ff7c98c68002352.png</Image>
    #           <Image>https://static-01.daraz.pk/p/97545b9b42e3a4781ff7c98c68002352.png</Image>
    # <brand>Remark</brand>
              
def create_new_product(access_token: str, product: DarazProductCreate):
    create_product_request = LazopRequest('/product/create')
    xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Request>
          <Product>
            <PrimaryCategory>{product.PrimaryCategory}</PrimaryCategory>
            <SPUId/>
            <AssociatedSku/>
            <Images>
              {''.join([f'<Image>{img}</Image>' for img in product.Images])}
            </Images>
            <Attributes>
              <name>{product.name}</name>
              <short_description>{product.short_description}</short_description>
              <short_description_en>{product.short_description}</short_description_en>
              <description>{product.description}</description>
              <description_en>{product.description}</description_en>
              <brand>{product.brand}</brand>
              <model>asdf</model>
              <kid_years>Kids (6-10yrs)</kid_years>
              <name_en>{product.name}</name_en>
              <occasion>Casual</occasion>
              <age_range>Standard</age_range>
              <warranty_type>No Warranty</warranty_type>
            </Attributes>
            <Skus>
              <Sku>
                <SellerSku>api-create-test-2</SellerSku>
                <color_family>Green</color_family>
                <size>40</size>
                <quantity>1</quantity>
                <price>389</price>
                <package_length>11</package_length>
                <package_height>22</package_height>
                <package_weight>33</package_weight>
                <package_width>44</package_width>
                <package_content>this is what's in the box</package_content>
                <Images>
                  <Image>https://static-01.daraz.pk/p/97545b9b42e3a4781ff7c98c68002352.png</Image>
                  <Image>https://static-01.daraz.pk/p/97545b9b42e3a4781ff7c98c68002352.png</Image>
                </Images>
              </Sku>
            </Skus>
          </Product>
        </Request>"""
        
    create_product_request.add_api_param('payload', xml_payload)
    response = lazop_client.execute(create_product_request, access_token)
    return JSONResponse({"type": response.type, "body": response.body})