from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form') #Quando alguém acessar essa rota, use oauth2_schema pra extrair o token JWT do header Authorization, e me entregue esse token como string na variável token.

from src.controller.service_auth.auth_routes import auth_router # noqa: E402
from src.controller.service_order.order_routes import order_router # noqa: E402

app.include_router(auth_router)
app.include_router(order_router)

