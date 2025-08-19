from pydantic import BaseModel, ConfigDict
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: bool
    admin: bool
    model_config = ConfigDict(from_attributes=True)