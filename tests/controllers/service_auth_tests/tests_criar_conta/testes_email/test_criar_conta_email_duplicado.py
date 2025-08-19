from main import fake, client
from pytest_bdd import scenario, given, when, then

@scenario('auth/create_account.feature', 'Criar conta com e-mail já existente')
def test_scenario_email_existente():
    """Conecta o cenário aos steps."""

@given('email de usuário já está cadastrado', target_fixture="payload")
def payload_email_duplicado():
    nome = fake.name()
    email = 'fabio@gmail.com'

    corpo_requisicao = {
        'nome': nome,
        'email': email,
        'senha': '123456',
        'ativo': True,
        'admin': False
    }

    return corpo_requisicao

@when('tentando criar a conta', target_fixture="response")
def criar_conta_email_duplicado(payload):
    return client.post('/auth/create_account', json=payload)

@then('o sistema deve retornar status code 409')
def verificar_status_code_409(response):
    status_code = response.status_code
    assert status_code == 409

@then('o sistema deve retornar o erro "Usuário ja existe"')
def retornar_erro_no_cadastro(response):
    dados_resposta = response.json()
    assert 'detail' in dados_resposta
    assert dados_resposta['detail'] == 'Usuário ja existe'