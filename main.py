#Importações SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

#Criação de engine para banco de dados SQLite e configuração da sessão
db = create_engine('sqlite:///banco_restaurante.db', echo=False)
Session = sessionmaker(bind=db)
session = Session()

#Classe base para definir as tabelas do banco de dados com SQLAlchemy
Base = declarative_base()

#Definicao das entidades do banco de dados

class Categoria(Base):
    __tablename__ = 'categorias'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nome_categoria = Column(String, nullable=False)

    #Relacionamento 1 para N com prato
    pratos = relationship("Prato", back_populates="categoria")

    #Representação da classe de maneira legível
    def __repr__(self):
        return f"<Categoria(id={self.id_categoria}, nome={self.nome_categoria})>"

class Prato(Base):
    __tablename__ = 'pratos'

    id_prato = Column(Integer, primary_key=True, autoincrement=True)
    nome_prato = Column(String, nullable=False)
    preco = Column(Integer, nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))

    #Relacionamento com a categoria
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

#Criação das tabelas no banco de dados
Base.metadata.create_all(bind=db)

#Operações CRUD (Create, Read, Update, Delete)

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

#Ler um registro pela ID

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
        print(f"Categoria {id_categoria} excluída com sucesso.")
    else:
        print(f"Categoria com ID {id_categoria} não encontrada.")

def excluir_prato(id_prato):
    prato = session.query(Prato).filter_by(id_prato=id_prato).first()
    if prato:
        session.delete(prato)
        session.commit()
        print(f"Prato {id_prato} excluído com sucesso.")
    else:
        print(f"Prato com ID {id_prato} não encontrado.")

def excluir_cliente(id_cliente):
    cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    if cliente:
        session.delete(cliente)
        session.commit()
        print(f"Cliente {id_cliente} excluído com sucesso.")
    else:
        print(f"Cliente com ID {id_cliente} não encontrado.")

def excluir_pedido(id_pedido):
    pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
    if pedido:
        session.delete(pedido)
        session.commit()
        print(f"Pedido {id_pedido} excluído com sucesso.")
    else:
        print(f"Pedido com ID {id_pedido} não encontrado.")

#Função para consultar todas as tabelas

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

#Funções para definir os menus para o usuário

def exibir_menu():
    print("--- MENU PRINCIPAL ---")
    print("1. Categorias")
    print("2. Pratos")
    print("3. Clientes")
    print("4. Pedidos")
    print("5. Consultar todas as tabelas")
    print("0. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_categoria():
    print("--- MENU CATEGORIAS ---")
    print("1. Criar categoria")
    print("2. Ler categoria")
    print("3. Atualizar categoria")
    print("4. Excluir categoria")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_prato():
    print("--- MENU PRATOS ---")
    print("1. Criar prato")
    print("2. Ler prato")
    print("3. Atualizar prato")
    print("4. Excluir prato")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_cliente():
    print("--- MENU CLIENTES ---")
    print("1. Criar cliente")
    print("2. Ler cliente")
    print("3. Atualizar cliente")
    print("4. Excluir cliente")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_pedido():
    print("--- MENU PEDIDOS ---")
    print("1. Criar pedido")
    print("2. Ler pedido")
    print("3. Atualizar pedido")
    print("4. Excluir pedido")
    opcao = input("Escolha uma opção: ")
    return opcao

#Função para o menu principal

def main():
    while True:
        opcao = exibir_menu()

        if opcao == '1': #Categorias
            escolha = menu_categoria()
            if escolha == '1': #Criar categoria
                nome_categoria = input("Digite o nome da nova categoria: ")
                criar_categoria(nome_categoria)
                print("Categoria criada com sucesso!")
            elif escolha == '2': #Ler categoria
                id_categoria = input("Digite o ID da categoria: ")
                categoria = ler_categoria(int(id_categoria))
                print(categoria)
            elif escolha == '3': #Atualizar categoria
                id_categoria = input("Digite o ID da categoria a ser atualizada: ")
                nome_categoria = input("Digite o novo nome da categoria: ")
                atualizar_categoria(int(id_categoria), nome_categoria)
                print("Categoria atualizada com sucesso!")
            elif escolha == '4': #Excluir categoria
                id_categoria = input("Digite o ID da categoria: ")
                if id_categoria.isdigit():
                    excluir_categoria(int(id_categoria))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")
        
        elif opcao == '2': #Pratos
            escolha = menu_prato()
            if escolha == '1': #Criar prato
                nome_prato = input("Digite o nome do novo prato: ")
                preco = input("Digite o preço do prato: ")
                id_categoria = input("Digite o ID da categoria do prato: ")
                criar_prato(nome_prato, int(preco), int(id_categoria))
                print("Prato criado com sucesso!")
            elif escolha == '2': #Ler prato
                id_prato = input("Digite o ID do prato: ")
                prato = ler_prato(int(id_prato))
                print(prato)
            elif escolha == '3': #Atualizar prato
                id_prato = input("Digite o ID do prato a ser atualizado: ")
                nome_prato = input("Digite o novo nome do prato (ou deixe vazio para não alterar): ")
                preco = input("Digite o novo preço do prato (ou deixe vazio para não alterar): ")
                id_categoria = input("Digite o novo ID da categoria (ou deixe vazio para não alterar): ")
                atualizar_prato(
                    int(id_prato),
                    nome_prato if nome_prato else None,
                    int(preco) if preco else None,
                    int(id_categoria) if id_categoria else None
                )
                print("Prato atualizado com sucesso!")
            elif escolha == '4': #Excluir prato
                id_prato = input("Digite o ID do prato: ")
                if id_prato.isdigit():
                    excluir_prato(int(id_prato))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")

        elif opcao == '3': #Clientes
            escolha = menu_cliente()
            if escolha == '1': #Criar cliente
                nome_cliente = input("Digite o nome do novo cliente: ")
                telefone = input("Digite o telefone do cliente: ")
                criar_cliente(nome_cliente, telefone)
                print("Cliente criado com sucesso!")
            elif escolha == '2': #Ler cliente
                id_cliente = input("Digite o ID do cliente: ")
                cliente = ler_cliente(int(id_cliente))
                print(cliente)
            elif escolha == '3': #Atualizar cliente
                id_cliente = input("Digite o ID do cliente a ser atualizado: ")
                nome_cliente = input("Digite o novo nome do cliente (ou deixe vazio para não alterar): ")
                telefone = input("Digite o novo telefone do cliente (ou deixe vazio para não alterar): ")
                atualizar_cliente(
                    int(id_cliente),
                    nome_cliente if nome_cliente else None,
                    telefone if telefone else None
                )
                print("Cliente atualizado com sucesso!")
            elif escolha == '4': #Excluir cliente
                id_cliente = input("Digite o ID do cliente: ")
                if id_cliente.isdigit():
                    excluir_cliente(int(id_cliente))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")

        elif opcao == '4': #Pedidos
            escolha = menu_pedido()
            if escolha == '1': #Criar pedido
                id_cliente = input("Digite o ID do cliente: ")
                id_prato = input("Digite o ID do prato: ")
                data_pedido = input("Digite a data do pedido (YYYY-MM-DD): ")
                criar_pedido(int(id_cliente), int(id_prato), date.fromisoformat(data_pedido))
                print("Pedido criado com sucesso!")
            elif escolha == '2': #Ler pedido
                id_pedido = input("Digite o ID do pedido: ")
                pedido = ler_pedido(int(id_pedido))
                print(pedido)
            elif escolha == '3': #Atualizar pedido
                id_pedido = input("Digite o ID do pedido a ser atualizado: ")
                id_cliente = input("Digite o novo ID do cliente (ou deixe vazio para não alterar): ")
                id_prato = input("Digite o novo ID do prato (ou deixe vazio para não alterar): ")
                data_pedido = input("Digite a nova data do pedido (YYYY-MM-DD) ou deixe vazio: ")
                atualizar_pedido(
                    int(id_pedido),
                    int(id_cliente) if id_cliente else None,
                    int(id_prato) if id_prato else None,
                    date.fromisoformat(data_pedido) if data_pedido else None
                )
                print("Pedido atualizado com sucesso!")
            elif escolha == '4': #Excluir pedido
                id_pedido = input("Digite o ID do pedido: ")
                if id_pedido.isdigit():
                    excluir_pedido(int(id_pedido))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")

        elif opcao == '5': #Consultar todas as tabelas
            consultar_todas_tabelas()

        elif opcao == '0': #Sair
            print("Saindo")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

#Executa o menu principal
main()