from pydantic import BaseModel, ConfigDict

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    model_config = ConfigDict(from_attributes=True)