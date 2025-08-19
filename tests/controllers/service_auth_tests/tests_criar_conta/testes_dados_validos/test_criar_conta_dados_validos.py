from main import fake, client
from pytest_bdd import scenario, given, when, then

@scenario('auth/create_account.feature', 'Criar conta com dados válidos')
def test_scenario_dados_validos():
    """Conecta o cenário aos steps."""

@given('usuário não existe', target_fixture="payload")
def payload_dados_validos() -> dict:
    nome = fake.name()
    username = fake.user_name()

    corpo_requicao = {
        'nome': nome,
        'email': f'{username}@gmail.com',
        'senha': '123456',
        'ativo': True,
        'admin': False
    }

    return corpo_requicao

@when("tento criar a conta", target_fixture="response")
def criar_conta(payload):
    return client.post("/auth/create_account", json=payload)
    

@then("o sistema deve retornar status code 200")
def verificar_status_code_200(response):
    print(response.json())
    assert response.status_code == 200

@then("o sistema deve retornar o usuario criado")
def verificar_usuario_criado(response, payload):
    dados_resposta = response.json()
    
    assert dados_resposta['nome'] == payload['nome']
    assert dados_resposta['email'] == payload['email']
    assert dados_resposta['mensagem'] == 'Usuário cadastrado com sucesso'

   

