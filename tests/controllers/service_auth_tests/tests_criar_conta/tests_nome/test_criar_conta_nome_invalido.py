from main import fake, client
from pytest_bdd import scenario, given, when, then

@scenario('auth/create_account.feature', 'Criar conta com nome inválido')
def test_scenario_email_existente():
    """Conecta o cenário aos steps."""

@given('usuario informa um nome inválido', target_fixture='payload')
def payload_nome_invalido():
    nome_invalido = 'a'
    email = fake.email()

    corpo_requisicao = {
        'nome': nome_invalido,
        'email': email,
        'senha': '123456',
        'ativo': True,
        'admin': False
    }

    return corpo_requisicao

@when('usuario tenta criar a conta', target_fixture='response')
def criar_conta_nome_invalido(payload):
    return client.post('/auth/create_account', json=payload)

@then('o sistema deve retornar status code 422')
def verificar_status_code(response):
    assert response.status_code == 422

@then('o sistema deve retornar um erro: "Nome inválida: o campo deve ter pelo menos 2 caracteres."')
def retornar_erro_no_cadastro(response):
    dados_resposta = response.json()

    assert 'detail' in dados_resposta
    assert dados_resposta['detail'] == 'Nome inválida: o campo deve ter pelo menos 2 caracteres.'