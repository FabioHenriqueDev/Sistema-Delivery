from src.dependencies.dependence import pegar_sessao
from src.model.models import Usuario
from main import fake

def test_criar_conta():
    sessao_generator = pegar_sessao()
    session = next(sessao_generator)  # pega a session do yield
    try:
        nome = fake.name()
        email = fake.email()
        usuario = Usuario(
                nome=nome, 
                email=email, 
                senha='1234', 
                ativo=True, 
                admin=False
            )
        session.add(usuario)
        session.commit()

        usuario_criado = session.query(Usuario).filter_by(email=email).first()

        assert usuario_criado is not None
        assert usuario_criado.nome == nome
        assert usuario_criado.email == email
        assert usuario_criado.ativo
        assert not usuario_criado.admin
    finally:
        session.close()




