from datetime import datetime, timedelta, timezone
from main import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
import jwt 

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_informacoes = {
        'sub': str(id_usuario),
        'exp': data_expiracao,
    }
    jwt_codificado = jwt.encode(dic_informacoes, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado


