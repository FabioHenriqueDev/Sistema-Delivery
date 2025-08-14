from pydantic import BaseModel, ConfigDict

class PedidoSchema(BaseModel):
    id_usuario: int
    model_config = ConfigDict(from_attributes=True)