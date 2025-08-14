from datetime import datetime, timedelta, timezone
from main import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, oauth2_schema
import jwt 
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from src.model.models import Usuario
from src.dependencies.dependence import pegar_sessao

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_informacoes = {
        'sub': str(id_usuario),
        'exp': data_expiracao,
    }
    jwt_codificado = jwt.encode(dic_informacoes, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado


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


