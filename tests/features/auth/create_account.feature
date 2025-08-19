Feature: Criar conta
  Testes de criar conta com todos os cenários possíveis do sistema

  Scenario: Criar conta com dados válidos
    Given usuário não existe
    When tento criar a conta
    Then o sistema deve retornar status code 200
    And o sistema deve retornar o usuario criado

  Scenario: Criar conta com e-mail já existente
    Given email de usuário já está cadastrado
    When tentando criar a conta
    Then o sistema deve retornar status code 409
    And o sistema deve retornar o erro "Usuário ja existe"
  
  Scenario: Criar conta com e-mail inválido
    Given o usuário informa um email inválido
    When tentando criar a conta
    Then o sistema deve retornar status code 422
    And o sistema deve retornar o erro "Email Inválido: email_invalido"

  Scenario: Criar conta com nome inválido
    Given usuario informa um nome inválido
    When usuario tenta criar a conta
    Then o sistema deve retornar status code 422
    And o sistema deve retornar um erro: "Nome inválida: o campo deve ter pelo menos 2 caracteres."
  
  

