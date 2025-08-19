from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from src.dependencies.database import get_engine


get_engine()
Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True)
    senha = Column('senha', String, nullable=False)
    ativo = Column('ativo', Boolean, nullable=False)
    admin = Column('admin', Boolean, nullable=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedidos(Base):
    __tablename__ = 'pedidos'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column('status', String) # pendente, cancelado, finalizado
    usuario = Column('usuario', ForeignKey('usuarios.id'))
    preco = Column('preco', Float)
    itens = relationship('ItemPedido', cascade='all, delete')

    def __init__(self, usuario, status='PENDENTE', preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco
    
    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        

class ItemPedido(Base):
    __tablename__ = 'itens_pedidos'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)
    preco_unitario = Column('preco_unitario', Float)
    pedido = Column('pedido', ForeignKey('pedidos.id'))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido