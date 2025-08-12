from pydantic import BaseModel

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True