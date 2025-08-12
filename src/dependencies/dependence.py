from sqlalchemy.orm import sessionmaker
from src.model.models import db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from src.model.models import Usuario
import jwt  # PyJWT
from jwt import PyJWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except PyJWTError as err:
        print(err)
        raise HTTPException(status_code=401, detail='Acesso Negado, verifique a validade do Token')
    
    usuario = session.query(Usuario).filter(Usuario.id == int(dic_info.get('sub'))).first()
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso Inválido') 
    return usuario