from fastapi import APIRouter, Depends, HTTPException
from src.model.models import Usuario
from sqlalchemy.orm import Session
from src.dependencies.dependence import pegar_sessao
from main import bcrypt_context
from src.schemas.usuario_schema.usuario_schema import UsuarioSchema
from src.schemas.login_schema.login_schema import LoginSchema
from src.security.jwt_handler import criar_token, verificar_token
from src.service.auth_service import autenticar_usuario
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.validate_email import validacao_email
from src.utils.validate_password import validate_senha
from src.utils.validate_name import validate_nome


auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.get('/')
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {'mensagem': 'Você acessou a rota de autentiocação', 'autenticado': False}


@auth_router.post('/create_account')
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter_by(email=usuario_schema.email).first()
    if not validate_nome(usuario_schema.nome):
        raise HTTPException(status_code=422, detail='Nome inválida: o campo deve ter pelo menos 2 caracteres.')
    if not validacao_email(usuario_schema.email):
        raise HTTPException(status_code=422, detail=f'Email Inválido: {usuario_schema.email}')
    if not validate_senha(usuario_schema.senha):
        raise HTTPException(status_code=422, detail='Senha inválida: o campo deve ter pelo menos 6 caracteres.')
    if usuario:
        raise HTTPException(status_code=409, detail="Usuário ja existe")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(
                nome=usuario_schema.nome, 
                email=usuario_schema.email, 
                senha=senha_criptografada, 
                ativo=usuario_schema.ativo,
                admin=usuario_schema.admin
            )
        session.add(novo_usuario)
        session.commit()
        return {
            'mensagem': 'Usuário cadastrado com sucesso',
            'nome': f'{novo_usuario.nome}',
            'email': f'{novo_usuario.email}'
        }
    

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
            }
    
@auth_router.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            'access_token': access_token,
            'token_type': 'Bearer'
            }

@auth_router.get('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
            'access_token': access_token,
            'token_type': 'Bearer'
            }

