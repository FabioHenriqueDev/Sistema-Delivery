# Sistema-Delivery 🚚

Sistema de delivery inclusivo desenvolvido com **FastAPI**, focado em autenticação de usuários, gerenciamento de pedidos e segurança. Este projeto inclui testes automatizados, validação de dados e boas práticas de desenvolvimento.

---

## Tecnologias Utilizadas ⚙️

* **Backend**: FastAPI, SQLAlchemy, Alembic

* **Banco de Dados**: SQLite (desenvolvimento) / Planejado PostgreSQL (produção)

* **Autenticação**: JWT

* **Testes**: pytest, pytest-bdd

* **Segurança**: BanditScan, PipAudit, RefCheck

* **Migrations**: Alembic para versionamento do banco de dados

* **Planejamento Futuro**: CI/CD, deploy em AWS EC2

---

## Funcionalidades ⭐

* ✔️ Cadastro e autenticação de usuários

* 📦 Criação, listagem e gerenciamento de pedidos

* 🔒 Validação de e-mail e senha (mínimo de 6 caracteres)

* 🔬 Testes automatizados cobrindo os cenários principais do sistema

* 🛡️ Relatórios de segurança com Bandit em formato HTML

* 🔗 Integração com banco de dados local para testes e desenvolvimento

---

## Instalação 💻

1. Clone o repositório:

git clone https://github.com/FabioHenriqueDev/Sistema-Delivery.git
cd Sistema-Delivery


2. Crie e ative um ambiente virtual:

python -m venv .venv


* No Linux/macOS:

  ```
  source .venv/bin/activate
  ```

* No Windows:

  ```
  .venv\Scripts\activate
  ```

3. Instale as dependências:

pip install -r requirements.txt


4. Configure o banco de dados e aplique as migrations:

alembic upgrade head


---

## Testes 🧪

O projeto utiliza **pytest** e **pytest-bdd** para testes unitários e BDD.

* Para rodar os testes:

pytest


* Relatórios de segurança podem ser gerados com **Bandit**:

bandit -r . -f html -o report.html


---

## Planejamento Futuro ✨

* Implementar CI/CD para integração e deploy contínuo

* Deploy do sistema em **AWS EC2**

* Cobertura completa de testes para todas as funcionalidades

* Melhorias na interface de usuário (frontend)