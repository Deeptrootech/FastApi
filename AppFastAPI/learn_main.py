# This Main file Includes Overall FastAPI Learning
import time

import jwt
from datetime import datetime, timedelta, timezone
from typing import List, Set, Union
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Form, File, UploadFile, HTTPException, Request, Depends, \
    status
from fastapi.encoders import jsonable_encoder
from typing_extensions import Annotated  # only if python <= 3.8.... otherwise can import from typing.
from pydantic import BaseModel, HttpUrl, Field, EmailStr
from typing import Any
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# **********************************************************************************************************************
# # 1)
# # Query Parameters and String Validations
# # (Validations karvu hatu etle 'Annotated' no use karyo other wise sidhu Typelass(here.. str | None) aapi shakai.)
# # (str | None) ma "or None" karyu e django ma Null=True (Field Not required) jevu  j chhe.
# @app.get("/items/", tags=["Query Parameters and String Validations"])
# async def read_items(
#         q: Annotated[
#             Union[str, None],  # if python = 3.10 (or above) then ---->  str | None
#             Query(
#                 alias="item-query",
#                 title="Query string",
#                 description="Query string for the items to search in the database that have a good match",
#                 min_length=3,
#                 max_length=50,
#                 pattern="^fixedquery$",
#                 # deprecated=True,
#             ),
#         ] = "None",
#         # Default value None aapi chhe... ahiya "deep" pan lakhi shakai.
#         # (To upar ni patter ne e ena related regex aapvu padse anhi to error aavse.)
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# **********************************************************************************************************************
# # 2)
# # Path Parameters and Numeric Validations
# # (Validations karvu hatu etle 'Annotated' no use karyo otherwise eni jagya e sidhu Typeclass(here.. int) aapi shakai.)
# @app.get("/items/{item_id}", tags=["Path Parameters and Numeric Validations"])
# async def read_items(
#         item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
#         q: Union[str, None] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# **********************************************************************************************************************
# # 3)
# # Body Multiple Parameters and Validations and Nested Body Pydantic Models
# class Image(BaseModel):
#     url: HttpUrl
#     name: str
#
#
# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = Field(
#         default=None, title="The description of the item", max_length=300
#     )  # you can add validations here... like we did in annotate's... path() and query()
#     price: float
#     tax: Union[float, None] = None
#     image: Union[Image, None] = None  # If Only One Image is linked (like... OneToOne/FK)
#     # image: Union[List[Image], None] = None  # If relation is like M2m & duplicated allowed
#     # image: Union[set[Image], None] = None  # If relation is like M2m & duplicated Not allowed
#
#
# class User(BaseModel):
#     username: str
#     full_name: Union[str, None] = None
#
#
# @app.put("/items/{item_id}", tags=["Body Multiple Parameters and Validations and Nested Body Pydantic Models"])
# async def update_item(
#         item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],  # path param
#         another_body_param: Annotated[int, Body()],
#         start_datetime: Annotated[datetime, Body()],
#         # Body params, because we added body().. otherwise It would have query_param
#         q: Union[str, None] = None,  # query param
#         item: Union[Item, None] = None,  # Body param, because we added typeclass as Pydantic model (here...Item)
#         user: Union[User, None] = None,  # Body param, because we added typeclass as Pydantic model (here...User)
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     if user:
#         results.update({"user": user})
#     if another_body_param or start_datetime:
#         results.update({"another_body_param": another_body_param, "start_datetime": start_datetime})
#     return results

# **********************************************************************************************************************
# # 4)
# # Cookie and Header parameters
# @app.get("/readcookie", tags=["Cookie parameters"])
# async def read_items(cookie_id: Annotated[Union[str, None], Cookie()] = None):
#     return {"ads_id": cookie_id}
#
#
# @app.get("/readheader/", tags=["Header parameters"])
# async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
#     return {"User-Agent": user_agent}

# **********************************************************************************************************************
# # 5) ********** confusion ***************
# # Response Model - (Return Type)
# # Use the path operation decorator's parameter response_model to define response models
# # and especially to ensure private data is filtered out.
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Union[str, None] = None
#
#
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Union[str, None] = None
#
#
# @app.post("/user", response_model=UserOut, tags=["Response Model - (Return Type)"])
# async def create_user(user: UserIn) -> Any:
#     return user

# **********************************************************************************************************************
# 6)
# Form Fields
# (i) request_payload will be ---> form-data
# (Do like this if you are directly receiving data from HTML form)
@app.post("/login_form", tags=["Form Fields (payload -> form-data)"])
async def login_form(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    print("password", password)
    return {"username": username}


# ****** Instead of defining every field... you can also use pydantic model.
# class FormData(BaseModel):
#     username: str
#     password: str
#
#
# @app.post("/login_form", tags=["Form Fields"])
# async def login_form(data: Annotated[FormData, Form()]):
#     return data


# (ii) request_payload will be ---> json
@app.post("/login_body", tags=["Form Fields (payload -> json)"])
async def login_body(username: Annotated[str, Body()], password: Annotated[str, Body()]):
    print("password", password)
    return {"username": username}


# 7)
# Request Files
# work for smaller size of files and stored entire file as a bytes in memory.
@app.post("/files", tags=["Request Files"])
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


# work for smaller and larger both size of files and A file stored as a file-like obj in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
@app.post("/uploadfile", tags=["Request Files"])
async def create_upload_file(file: Annotated[UploadFile, File(description="A file read as UploadFile")]):
    return {"filename": file.filename}


# 6) and 7) recap
# Use File and Form together when you need to receive form-data and files in the same request.
@app.post("/files_form", tags=["Request Files & Forms"])
async def create_file_form(
        file: Annotated[bytes, File()],  # file upload (save as bytes)
        fileb: Annotated[UploadFile, File()],  # file upload (save as file obj)
        token: Annotated[str, Form()],  # form data
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

# Warning (For above) --  see same at (https://fastapi.tiangolo.com/tutorial/request-forms-and-files/#recap)
# You can declare multiple File and Form parameters in a path operation,
# but you can't also declare Body fields that you expect to receive as JSON,
# as the request will have the body encoded using multipart/form-data instead of application/json.
# (This is not a limitation of FastAPI, it's part of the HTTP protocol.)

# **********************************************************************************************************************
# # 8) Handling Exception
# # (i) Handling with predefined Exception-handler.
# items = {"foo": "The foo wrestlers"}
#
#
# @app.get("/exception_handling", tags=["Handling Exception"])
# async def read_items_with_exception(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Given item not found",
#                             headers={"custom-error-header-key": "here goes my error"})
#     return {"item_id": item_id}
#
#
# # (ii) Handling Default Exception with custom Exception-handler.
# # This is default Exception and below written is custom_handler to modify message.
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):  # will be triggred when 418 or 404 generated.
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.get("/custom_handler", tags=["Handling Exception"])
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}
#
#
# # (iii) Handling custom Exception with custom Exception-handler.
# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name
#
#
# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )
#
#
# @app.get("/custom_exception_and_handler", tags=["Handling Exception"])
# async def read_unicorn(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}

# **********************************************************************************************************************
# # 9) JSON Compatible Encoder (From Paydantic obj -> json data)
# fake_db = {}
#
#
# class ItemModel(BaseModel):
#     title: str
#     timestamp: datetime
#     description: Union[str, None] = None
#
#
# @app.put("/paydantic_to_json/{item_id}", tags=["Paydantic obj -> json data"])
# def update_item(item_id: str, item: ItemModel):
#     """
#     It would convert the Pydantic model to a dict, and the datetime to a str and save to db (here, fake_db).
#     - Path param item_id:
#     - Body param item:
#     - return: item -> ItemModel
#     """
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[item_id] = json_compatible_item_data
#     return item

# **********************************************************************************************************************
# # 10) Body - Updates
#
# class ItemModel(BaseModel):
#     name: Union[str, None] = None
#     description: Union[str, None] = None
#     price: Union[float, None] = None
#     tax: float = 10.5
#     tags: List[str] = []
#
#
# items_db = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 12.5, "tags": []},
# }
#
#
# @app.get("/retrieve_items/{item_id}", response_model=ItemModel, tags=["Body - Updates"])
# async def read_item(item_id: str):
#     return items_db[item_id]
#
#
# @app.patch("/update_items/{item_id}", response_model=ItemModel, tags=["Body - Updates"])
# async def update_item(item_id: str, item: ItemModel):
#     """
#     The problem in this example is...
#     - If We had passed item(body param to update)
#     like...
#     {
#         "name": "Barz",
#         "price": 3,
#         "description": null
#     }  (only this fields should get updated... rest should be un-touched.)
#     - ... because it doesn't include the already stored attribute "tax": 20.2, the input model would take the default value of "tax": 10.5.
#     - And the data would be saved with that "new" tax of 10.5.
#     - like...
#     {
#         "name": "Barz",
#         "price": 3,
#         "description": None,
#         "tax": 10.5,
#         "tags": []
#     }
#
#     - EVEN IF WE ARE USING PATCH... next Example is solution for above problem
#     """
#     update_item_encoded = jsonable_encoder(item)
#     items_db[item_id] = update_item_encoded
#     return update_item_encoded
#
#
# @app.patch("/update_items_with_exclude_unset/{item_id}", tags=["Body - Updates"])
# async def update_item_exclude_unset(item_id: str, item: ItemModel):
#     """
#     Solution of Above Problem.
#     """
#     stored_item_data = items_db[item_id]
#     stored_item_model = ItemModel(**stored_item_data)
#     update_data = item.model_dump(exclude_unset=True)
#     updated_item = stored_item_model.model_copy(update=update_data)
#     items_db[item_id] = jsonable_encoder(updated_item)
#     return updated_item

# **********************************************************************************************************************
# # 11.1) Dependencies (Dependency Injection)
# # Need: (i) Have shared logic (the same code logic again and again).
#
# # ****** Function as Dependencies *******
# async def common_function(q: Annotated[Union[str, None], Query()] = None):
#     """
#     This is common Function.
#     """
#     return {"q_param": q}
#
#
# @app.get("/get_item_fun")
# async def read_item(commons: Annotated[dict, Depends(common_function)]):
#     return commons
#
#
# @app.get("/get_user_fun")
# async def read_user(commons: Annotated[dict, Depends(common_function)]):
#     return commons
#
#
# # ****** Class as Dependencies *******
# class CommonQueryParams:
#     def __init__(self, q: Union[str, None] = None):
#         self.var_q = q
#
#
# @app.get("/get_item_class")
# async def read_item(class_commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
#     return class_commons

# **********************************************************************************************************************
# # 11.2) Dependencies (Dependency Injection)
# Sub Dependencies. --> nested Dependency (like... multilevel Inheritence)
# Dependencies in path operation decorators --> you can define dependecy in path decorators rather in with function params.
# (If Necessary then Explore further in dependency dection)


# **********************************************************************************************************************
# # 12) Security.
# (i) with fake_hash_password

# fake_users_db = {
#     "johndoe": dict(
#         username="johndoe",
#         full_name="John Doe",
#         email="johndoe@example.com",
#         hashed_password="fakehashedsecret",
#         is_disabled=False,
#     ),
#     "alice": dict(
#         username="alice",
#         full_name="Alice Wonderson",
#         email="alice@example.com",
#         hashed_password="fakehashedsecret2",
#         is_disabled=True,
#     ),
# }
#
#
# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     fullname: Union[str, None] = None
#     is_disabled: Union[bool, None] = True
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="my_generate_token")
#
#
# @app.post("/my_generate_token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if hashed_password != user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# def fake_hash_password(password: str):
#     return "fakehashed" + password
#
#
# def get_decoded_user(db, token: str):
#     db_user = db.get(token)
#     return UserInDB(**db_user)
#
#
# async def get_current_user(user_token: Annotated[str, Depends(oauth2_scheme)]):
#     user = get_decoded_user(fake_users_db, user_token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: Annotated[str, Depends(get_current_user)]):
#     if current_user.is_disabled:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Inactive user",
#         )
#     return current_user
#
#
# @app.get("/read_myself")
# async def read_myself(current_active_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_active_user

# ****************************************************************************
# (ii) with JWT Token

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }
#
#
# # Paydantic models
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     username: Union[str, None] = None
#
#
# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# # Authorize_API: STEP:3  *** token Generate ***
# # IMPS:
# # (i) tokenUrl="token" is just a configuration for documentation and clarity.
# #     Informs Just clients and tools (like Swagger) where to fetch a token during login. (The Swagger documentation won’t know where to send the request to fetch a token.)
# #     It does not trigger any automatic call to /token.
# # (ii) If you omit the tokenUrl parameter: The Swagger documentation won’t know where to send the request to fetch a token.
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # tokenUrl="token": just to work with swagger Authorize Button.
# # (iii) 'OAuth2PasswordBearer' job is just to extract and validate the JWT token from the request's Authorization header in your FastAPI application.
# # *** End token Generate ***
#
# # *** Password Hashing, verify hashed with db's password ***
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password: str):
#     return pwd_context.hash(password)
#
#
# # *** End Password Hashing ***
#
#
# #  STEP:  *** Generate JWT Token ***
# # to get a string like this run: openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# REFRESH_SECRET_KEY = "385a608a787dfa2b43490a52661420447d85232704f81eab1358103bc3b4f019"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
#
#
# # Login_API (Generate Token): STEP:3
# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# # *** End Generate JWT Token ***
#
# #  *** authenticate_user, login and generate Token After logged-In ***
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# # Login_API (Generate Token): STEP:2
# def authenticate_user(fake_db, username: str, password: str):
#     """
#     Checking that If we are having same username and password into DB which user entered.
#     """
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# # Login_API (Generate Token): STEP:1,4(last)
# @app.post("/token")
# async def login_for_access_token(
#         form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     """
#     - Verify the user's credentials (username and password).
#     - Generate and return a new JWT token.
#     """
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")
#
#
# # *** End authenticate_user, login and generate Token After logged-In ***
#
# # Authorize_API: STEP:2,4  *** Get current authenticated user ***
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(
#         current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# # *** Protected APIs ***
# # Authorize_API: STEP:1,5(last)
# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#         current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user
#
#
# @app.get("/users/me/items/")
# async def read_own_items(
#         current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]


# **********************************************************************************************************************
# # 13) Middleware.
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     total_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(total_time)
#     return response
#
#
# @app.get("/blah")
# async def my_blah_func():
#     return {"name": "deep"}

# **********************************************************************************************************************
# # 14) CORS (Cross-Origin Resource Sharing)
#
# origins = [
#     "http://localhost:8000",
#     "http://localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
#
#
# @app.get("/")
# async def main():
#     return {"message": "Hello World"}
