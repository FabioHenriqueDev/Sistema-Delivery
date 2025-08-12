# 🍔 Sistema de Delivery - API

Este projeto é uma **API para gerenciamento de pedidos em um sistema de delivery**, desenvolvida com **FastAPI** e **SQLAlchemy**.  
O objetivo é permitir que usuários autenticados realizem pedidos, visualizem e gerenciem seus itens, além de manter um fluxo seguro de autenticação e autorização.

---

## 🚀 Funcionalidades

- 🔑 **Autenticação JWT**  
  Apenas usuários autenticados podem criar pedidos, garantindo a segurança dos dados.

- 📦 **Gerenciamento de Pedidos**  
  - Criar pedidos  
  - Adicionar e remover itens  
  - Recalcular automaticamente o valor total do pedido  

- ⚙ **Automação com Makefile**  
  Utilização de comandos no `Makefile` para agilizar tarefas, como:  
  - Criar ou resetar o banco de dados  
  - Executar migrations  
  - Subir o servidor  
  - Limpar arquivos temporários  

- 🗄 **Migrations com Alembic**  
  Controle de versão do banco de dados, permitindo evolução estruturada das tabelas.

---

## 📋 Pré-requisitos

- Python 3.10+  
- Pip  
- Virtualenv (opcional, mas recomendado)  
- SQLite ou outro banco configurado no `SQLAlchemy`  

---

## ⚙️ Instalação

Clone este repositório:

```bash
git clone https://github.com/seu-usuario/sistema-delivery.git
cd sistema-delivery

## Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
