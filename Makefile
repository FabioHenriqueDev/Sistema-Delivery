run:
	uvicorn main:app --reload

# Isso gera um novo arquivo de migration script dentro da pasta versions/.
init-migration:
	alembic revision --autogenerate -m "$(M)"

# Isso atualiza o banco de dados de acordo com as alterações detectadas nos seus modelos SQLAlchemy.
migrate-up:
	alembic upgrade head

# Mostra o histórico de migrations
migration-history:
	alembic history --verbose

# Mostra o status atual das migrations aplicadas
migration-status:
	alembic current

requirements:
	pip freeze > requirements.txt

upgrade-requirements:
	pip install --upgrade -r requirements.txt

upgrade-tools:
	python -m pip install --upgrade pip setuptools

lint:
	ruff check .

check:
	pip-audit

bandit-scan:
	bandit -r src main.py --exclude .venv

bandit-html:
	bandit -r src main.py --exclude .venv -f html -o bandit_report.html