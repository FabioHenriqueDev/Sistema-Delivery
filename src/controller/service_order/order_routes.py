from fastapi import APIRouter, Depends, HTTPException
from src.dependencies.dependence import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from src.schemas.pedido_shema.pedido_schema import PedidoSchema
from src.schemas.item_pedido_schema.item_pedido_schema import ItemPedidoSchema
from src.model.models import Pedidos, Usuario, ItemPedido

order_router = APIRouter(prefix='/orders', tags=['orders'], dependencies=[Depends(verificar_token)])

@order_router.get('/')
async def pedidos():
    """
    Essa rota é a rota padrão de pedidos e precisam estar autenticados
    """
    return {"mensagem": "Você acessou a rota de pedidos"}


@order_router.post('/create_oder')# adicionar paar cada usuario criar um pedido para a conta dele
async def criar_pedidos(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    usuario_inexistente= session.query(Usuario).filter_by(id=usuario.id).first()
    if not usuario_inexistente:
        raise HTTPException(404, detail='Esse usuário não existe')
    novo_pedido = Pedidos(usuario=usuario.id)
    session.add(novo_pedido)
    session.commit()
    return {
        'mensagem': f'Pedido número: {novo_pedido.id} criado com sucesso',
        'pedido': novo_pedido
    } 


@order_router.post('/create_oder/admin')
async def criar_pedidos_admin(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(403, detail='Você não tem autorização para isso')
    usuario_inexistente= session.query(Usuario).filter_by(id=pedido_schema.id_usuario).first()
    if not usuario_inexistente:
        raise HTTPException(404, detail='Esse usuário não existe')
    novo_pedido = Pedidos(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {
        'mensagem': f'Pedido número: {novo_pedido.id} criado com sucesso',
        'pedido': novo_pedido
    } 


@order_router.post('/order/cancel/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido_usuario = session.query(Pedidos).filter(Pedidos.id==id_pedido).first()
    if not pedido_usuario:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    if usuario.id != pedido_usuario.usuario and not usuario.admin:
        raise HTTPException(status_code=401, detail='Você não tem autorização para fazer essa modificação')
    pedido_usuario.status = 'CANCELADO'
    session.commit()
    return {
            'mensagem': f'Pedido número: {pedido_usuario.id} cancelado com sucesso',
            'pedido': pedido_usuario
        }


@order_router.get('/list')
async def listar_pedidos(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedidos_usuario = session.query(Pedidos).filter_by(usuario=usuario.id).all()
    print(pedidos_usuario)
    if not pedidos_usuario:
        raise HTTPException(status_code=404, detail='Você não tem pedidos para serem listados')
    return [pedido for pedido in pedidos_usuario]


@order_router.get('/list/{id_pedido}')
async def listar_pedido_por_id(id_pedido, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido_usuario = session.query(Pedidos).filter_by(id=id_pedido).first()
    if not pedido_usuario:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    elif pedido_usuario.usuario != usuario.id and not usuario.admin:
        raise HTTPException(status_code=403, detail='Você não tem permissão para isso')
    return {
        'itens_pedido': len(pedido_usuario.itens),
        'pedido': pedido_usuario
    }


@order_router.get('/list-admin/{id_usuario}')
async def listar_pedidos_admin(id_usuario: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail='Você não tem permissão para isso')
    pedidos_usuario = session.query(Pedidos).filter_by(usuario=id_usuario).all()
    if not pedidos_usuario:
        raise HTTPException(status_code=404, detail='Nenhum pedido encontrado')
    return [pedido for pedido in pedidos_usuario]
    

@order_router.post('/order/add-item/{id_pedido}')
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedidos).filter_by(id=id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    elif pedido.usuario != usuario.id and not usuario.admin:
        raise HTTPException(status_code=403, detail='Você não tem permissão para isso')  
    elif pedido.status == 'CANCELADO':
        raise HTTPException(status_code=409, detail='Você não pode adicionar um item em um pedido cancelado')
    
    item_pedido = ItemPedido(
        quantidade=item_pedido_schema.quantidade,
        sabor=item_pedido_schema.sabor,
        tamanho=item_pedido_schema.tamanho,
        preco_unitario=item_pedido_schema.preco_unitario,
        pedido=id_pedido
    )
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        'mensagem': 'Item de Pedido adcionado com sucesso',
        'item_id': item_pedido.id,
        'preco_pedido': pedido.preco
    }

# !
@order_router.delete('/order/remove-item/{id_item_pedido}')
async def remover_item_pedido(id_item_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    item_pedido = session.query(ItemPedido).filter_by(id=id_item_pedido).first()
    pedido = session.query(Pedidos).filter_by(id=item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=404, detail='Item do pedido não encontrado')
    elif not pedido:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail='Você não tem permissão para isso')
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
            'mensagem': 'Item removido com sucesso',
            'quantidades_itens_pedido': len(pedido.itens),
            'pedido': pedido
        }


@order_router.get('/order/finish/{id_pedido}')
async def finalizar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedidos).filter_by(id=id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido não encontrado')
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail='Você não tem permissão para isso')
    elif pedido.status == 'CANCELADO':
        raise HTTPException(status_code=409, detail='Você não pode finalizar um pedido cancelado')
    pedido.status = 'FINALIZADO'
    session.commit()
    return {
            'mensagem': f'Pedido número {pedido.id} finalizado com sucesso',
            'quantidades_itens_pedido': len(pedido.itens),
            'pedido': pedido
        }