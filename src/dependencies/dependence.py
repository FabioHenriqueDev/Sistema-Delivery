from sqlalchemy.orm import sessionmaker
from src.dependencies.database import get_engine

def pegar_sessao():
    try:
        Session = sessionmaker(bind=get_engine())
        session = Session()
        yield session
    finally:
        session.close()


