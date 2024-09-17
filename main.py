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

def exibir_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Categorias")
    print("2. Pratos")
    print("3. Clientes")
    print("4. Pedidos")
    print("5. Consultar todas as tabelas")
    print("0. Sair")
    return input("Escolha uma opção: ")

def menu_categoria():
    print("\n--- MENU CATEGORIAS ---")
    print("1. Criar categoria")
    print("2. Ler categoria")
    print("3. Atualizar categoria")
    print("4. Excluir categoria")
    return input("Escolha uma opção: ")

def menu_prato():
    print("\n--- MENU PRATOS ---")
    print("1. Criar prato")
    print("2. Ler prato")
    print("3. Atualizar prato")
    print("4. Excluir prato")
    return input("Escolha uma opção: ")

def menu_cliente():
    print("\n--- MENU CLIENTES ---")
    print("1. Criar cliente")
    print("2. Ler cliente")
    print("3. Atualizar cliente")
    print("4. Excluir cliente")
    return input("Escolha uma opção: ")

def menu_pedido():
    print("\n--- MENU PEDIDOS ---")
    print("1. Criar pedido")
    print("2. Ler pedido")
    print("3. Atualizar pedido")
    print("4. Excluir pedido")
    return input("Escolha uma opção: ")

def main():
    while True:
        opcao = exibir_menu()

        if opcao == '1':  # Categorias
            escolha = menu_categoria()
            if escolha == '1':
                nome_categoria = input("Digite o nome da categoria: ")
                criar_categoria(nome_categoria)
                print("Categoria criada com sucesso!")
            elif escolha == '2':
                id_categoria = int(input("Digite o ID da categoria: "))
                categoria = ler_categoria(id_categoria)
                print(categoria if categoria else "Categoria não encontrada.")
            elif escolha == '3':
                id_categoria = int(input("Digite o ID da categoria: "))
                nome_categoria = input("Digite o novo nome da categoria: ")
                atualizar_categoria(id_categoria, nome_categoria)
                print("Categoria atualizada com sucesso!")
            elif escolha == '4':
                id_categoria = int(input("Digite o ID da categoria: "))
                excluir_categoria(id_categoria)
                print("Categoria excluída com sucesso!")
        
        elif opcao == '2':  # Pratos
            escolha = menu_prato()
            if escolha == '1':
                nome_prato = input("Digite o nome do prato: ")
                preco = int(input("Digite o preço do prato: "))
                id_categoria = int(input("Digite o ID da categoria: "))
                criar_prato(nome_prato, preco, id_categoria)
                print("Prato criado com sucesso!")
            elif escolha == '2':
                id_prato = int(input("Digite o ID do prato: "))
                prato = ler_prato(id_prato)
                print(prato if prato else "Prato não encontrado.")
            elif escolha == '3':
                id_prato = int(input("Digite o ID do prato: "))
                nome_prato = input("Digite o novo nome do prato: ")
                preco = input("Digite o novo preço do prato: ")
                preco = int(preco) if preco else None
                id_categoria = input("Digite o novo ID da categoria: ")
                id_categoria = int(id_categoria) if id_categoria else None
                atualizar_prato(id_prato, nome_prato, preco, id_categoria)
                print("Prato atualizado com sucesso!")
            elif escolha == '4':
                id_prato = int(input("Digite o ID do prato: "))
                excluir_prato(id_prato)
                print("Prato excluído com sucesso!")
        
        elif opcao == '3':  # Clientes
            escolha = menu_cliente()
            if escolha == '1':
                nome_cliente = input("Digite o nome do cliente: ")
                telefone = input("Digite o telefone do cliente: ")
                criar_cliente(nome_cliente, telefone)
                print("Cliente criado com sucesso!")
            elif escolha == '2':
                id_cliente = int(input("Digite o ID do cliente: "))
                cliente = ler_cliente(id_cliente)
                print(cliente if cliente else "Cliente não encontrado.")
            elif escolha == '3':
                id_cliente = int(input("Digite o ID do cliente: "))
                nome_cliente = input("Digite o novo nome do cliente: ")
                telefone = input("Digite o novo telefone do cliente: ")
                atualizar_cliente(id_cliente, nome_cliente, telefone)
                print("Cliente atualizado com sucesso!")
            elif escolha == '4':
                id_cliente = int(input("Digite o ID do cliente: "))
                excluir_cliente(id_cliente)
                print("Cliente excluído com sucesso!")
        
        elif opcao == '4':  # Pedidos
            escolha = menu_pedido()
            if escolha == '1':
                id_cliente = int(input("Digite o ID do cliente: "))
                id_prato = int(input("Digite o ID do prato: "))
                data_pedido = date.today()
                criar_pedido(id_cliente, id_prato, data_pedido)
                print("Pedido criado com sucesso!")
            elif escolha == '2':
                id_pedido = int(input("Digite o ID do pedido: "))
                pedido = ler_pedido(id_pedido)
                print(pedido if pedido else "Pedido não encontrado.")
            elif escolha == '3':
                id_pedido = int(input("Digite o ID do pedido: "))
                id_cliente = input("Digite o novo ID do cliente: ")
                id_cliente = int(id_cliente) if id_cliente else None
                id_prato = input("Digite o novo ID do prato: ")
                id_prato = int(id_prato) if id_prato else None
                data_pedido = input("Digite a nova data do pedido (AAAA-MM-DD): ")
                data_pedido = date.fromisoformat(data_pedido) if data_pedido else None
                atualizar_pedido(id_pedido, id_cliente, id_prato, data_pedido)
                print("Pedido atualizado com sucesso!")
            elif escolha == '4':
                id_pedido = int(input("Digite o ID do pedido: "))
                excluir_pedido(id_pedido)
                print("Pedido excluído com sucesso!")

        elif opcao == '5':  # Consultar todas as tabelas
            consultar_todas_tabelas()

        elif opcao == '0':  # Sair
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    main()
