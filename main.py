from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

db = create_engine('sqlite:///banco_restaurante.db', echo=False)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

#Definicao das entidades do banco de dados

class Categoria(Base):
    __tablename__ = 'categorias'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nome_categoria = Column(String, nullable=False)

    pratos = relationship("Prato", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id_categoria}, nome={self.nome_categoria})>"

class Prato(Base):
    __tablename__ = 'pratos'

    id_prato = Column(Integer, primary_key=True, autoincrement=True)
    nome_prato = Column(String, nullable=False)
    preco = Column(Integer, nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))

    categoria = relationship("Categoria", back_populates="pratos")

    def __repr__(self):
        return f"<Prato(id={self.id_prato}, nome={self.nome_prato}, preco={self.preco})>"

class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    def __repr__(self):
        return f"<Cliente(id={self.id_cliente}, nome={self.nome_cliente}, telefone={self.telefone})>"

class Pedido(Base):
    __tablename__ = 'pedidos'

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    id_prato = Column(Integer, ForeignKey('pratos.id_prato'))
    data_pedido = Column(Date)

    cliente = relationship("Cliente")
    prato = relationship("Prato")

    def __repr__(self):
        return f"<Pedido(id={self.id_pedido}, cliente={self.id_cliente}, prato={self.id_prato}, data={self.data_pedido})>"

Base.metadata.create_all(bind=db)

#Criar

def criar_categoria(nome_categoria):
    nova_categoria = Categoria(nome_categoria=nome_categoria)
    session.add(nova_categoria)
    session.commit()
    return nova_categoria

def criar_prato(nome_prato, preco, id_categoria):
    novo_prato = Prato(nome_prato=nome_prato, preco=preco, id_categoria=id_categoria)
    session.add(novo_prato)
    session.commit()
    return novo_prato

def criar_cliente(nome_cliente, telefone):
    novo_cliente = Cliente(nome_cliente=nome_cliente, telefone=telefone)
    session.add(novo_cliente)
    session.commit()
    return novo_cliente

def criar_pedido(id_cliente, id_prato, data_pedido):
    novo_pedido = Pedido(id_cliente=id_cliente, id_prato=id_prato, data_pedido=data_pedido)
    session.add(novo_pedido)
    session.commit()
    return novo_pedido

#Ler um registro específico

def ler_categoria(id_categoria):
    return session.query(Categoria).filter_by(id_categoria=id_categoria).first()

def ler_prato(id_prato):
    return session.query(Prato).filter_by(id_prato=id_prato).first()

def ler_cliente(id_cliente):
    return session.query(Cliente).filter_by(id_cliente=id_cliente).first()

def ler_pedido(id_pedido):
    return session.query(Pedido).filter_by(id_pedido=id_pedido).first()

#Ler todos os registros
#Exemplo de print:
#clientes =ler_todos_clientes()
#for cliente in clientes:
    #print(cliente)

def ler_todos_clientes():
    return session.query(Cliente).all()

def ler_todos_pratos():
    return session.query(Prato).all()

def ler_todas_categorias():
    return session.query(Categoria).all()

def ler_todos_pedidos():
    return session.query(Pedido).all()

#Atualizar

def atualizar_categoria(id_categoria, nome_categoria):
    categoria = session.query(Categoria).filter_by(id_categoria=id_categoria).first()
    if categoria:
        categoria.nome_categoria = nome_categoria
        session.commit()
    return categoria

def atualizar_prato(id_prato, nome_prato=None, preco=None, id_categoria=None):
    prato = session.query(Prato).filter_by(id_prato=id_prato).first()
    if prato:
        if nome_prato is not None:
            prato.nome_prato = nome_prato
        if preco is not None:
            prato.preco = preco
        if id_categoria is not None:
            prato.id_categoria = id_categoria
        session.commit()
    return prato

def atualizar_cliente(id_cliente, nome_cliente=None, telefone=None):
    cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    if cliente:
        if nome_cliente is not None:
            cliente.nome_cliente = nome_cliente
        if telefone is not None:
            cliente.telefone = telefone
        session.commit()
    return cliente

def atualizar_pedido(id_pedido, id_cliente=None, id_prato=None, data_pedido=None):
    pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
    if pedido:
        if id_cliente is not None:
            pedido.id_cliente = id_cliente
        if id_prato is not None:
            pedido.id_prato = id_prato
        if data_pedido is not None:
            pedido.data_pedido = data_pedido
        session.commit()
    return pedido

#Excluir

def excluir_categoria(id_categoria):
    categoria = session.query(Categoria).filter_by(id_categoria=id_categoria).first()
    if categoria:
        session.delete(categoria)
        session.commit()

def excluir_prato(id_prato):
    prato = session.query(Prato).filter_by(id_prato=id_prato).first()
    if prato:
        session.delete(prato)
        session.commit()

def excluir_cliente(id_cliente):
    cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    if cliente:
        session.delete(cliente)
        session.commit()

def excluir_pedido(id_pedido):
    pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
    if pedido:
        session.delete(pedido)
        session.commit()

#Funcao para printar todas as tabelas
def consultar_todas_tabelas():

    print("Categorias:")
    categorias = session.query(Categoria).all()
    if categorias:
        for categoria in categorias:
            print(f"{categoria}")
    else:
        print("Nenhuma categoria cadastrada.")

    print("Pratos:")
    pratos = session.query(Prato).all()
    if pratos:
        for prato in pratos:
            print(f"{prato}")
    else:
        print("Nenhum prato cadastrado.")

    print("Clientes:")
    clientes = session.query(Cliente).all()
    if clientes:
        for cliente in clientes:
            print(f"{cliente}")
    else:
        print("Nenhum cliente cadastrado.")

    print("Pedidos:")
    pedidos = session.query(Pedido).join(Cliente).join(Prato).all()
    if pedidos:
        for pedido in pedidos:
            print(f"Pedido {pedido.id_pedido}: Cliente {pedido.cliente.nome_cliente}, "
                  f"Prato {pedido.prato.nome_prato}, Data {pedido.data_pedido}")
    else:
        print("Nenhum pedido cadastrado.")