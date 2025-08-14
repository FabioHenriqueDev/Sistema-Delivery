from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

def get_engine():
    load_dotenv()
    
    ambiente_test = os.getenv("APP_ENV") == "true"
    
    if ambiente_test:
        db_path = 'database_test/test_database.db'
    else:
        db_path = 'database/banco.db'

    db_url = f"sqlite:///{db_path}"
    print(db_url)
    return create_engine(db_url, echo=True)