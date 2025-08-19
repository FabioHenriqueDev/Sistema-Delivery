from main import fake, client
from pytest_bdd import scenario, given, when, then

@scenario('auth/create_account.feature', 'Criar conta com e-mail inválido')
def test_scenario_email_invalido():
    """Conecta o cenário aos steps."""

@given('o usuário informa um email inválido', target_fixture="payload")
def payload_email_invalido():
    nome = fake.name()
    email_invalido = 'email_invalido'

    corpo_requisicao = {
        'nome': nome,
        'email': email_invalido,
        'senha': '123456',
        'ativo': True,
        'admin': False
    }

    return corpo_requisicao


@when('tentando criar a conta', target_fixture="response")
def criar_conta_email_invalido(payload):
    return client.post('/auth/create_account', json=payload)

@then('o sistema deve retornar status code 422')
def verificar_status_code_422(response):
    assert response.status_code == 422

@then('o sistema deve retornar o erro "Email Inválido: email_invalido"')
def verificar_erro_email_invalido(response, payload):
    dados_resposta = response.json()
    assert 'detail' in dados_resposta
    assert dados_resposta['detail'] == f'Email Inválido: {payload["email"]}'
