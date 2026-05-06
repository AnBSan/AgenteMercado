from langchain.tools import BaseTool, tool
from tables import Produto, Cliente, Session

@tool
def cadastrar_produto(nome: str, preco: float, quantidade: int = 0):
    """Criar um novo produto no banco de dados, usada quando o usuário pedir para cadastrar um novo produto"""
    session = Session()
    try: 
        """ Usa os parâmetros passados (nome, preço e quantidade) e insere na tabela de produtos"""
        novo_produto = Produto(nome=nome, preco=preco, quantidade=quantidade)
        session.add(novo_produto)
        session.commit()
        return f'O produto {nome} foi adicionado com sucesso!'
    
    except Exception as e:
        return f'Erro ao criar o produto. {str(e)}'
    
    finally:
        session.close()

@tool
def atualizar_estoque(produto_id: int, nova_quantidade: int) -> str:
    """Atualizar o estoque, usada quando o usuário pedir para atualizar o estoque de algum produto"""
    session = Session()
    try:
        """seleciona o produto pelo id"""
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            return f'Produto com id {produto_id} não encontrado'
        
        """Define a nova quantidade"""
        nome_produto = produto.nome
        produto.quantidade = nova_quantidade
        session.commit()
        return f'O estoque do produto {nome_produto} foi atualizado para {nova_quantidade}!'
    except Exception as e:
        session.rollback()
        return f'Erro ao atualizar o estoque {str(e)}'
    finally:
        session.close()

@tool
def listar_produtos():
    """Lista todos os produtos cadastrados, usada quando o usuário pedir para litar todos os produtos já cadastrados"""
    session = Session()
    try:
        """ Busca e lista todos os produtos presentes na tabela"""
        produtos = session.query(Produto).all()
        if not produtos:
            return 'Nenhum produto encontrado!'
        session.commit()
        return '\n'.join([f'Id: {p.id}, Nome: {p.nome}, Preço: {p.preco:.2f}, Quantidade: {p.quantidade}' for p in produtos])
    finally:
        session.close()

@tool
def deletar_produto(produto_id: int) -> str:
    """Deleta o produto informado, usada quando o usuário pedir para deletar algum produto da tabela de Produtos.
    Sempre checar se realmente o usuário quer deletar o produto para evitar erros"""
    session = Session()
    try:
        """Seleciona o produto pelo id"""
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            return 'Produto não encontrado!'
        
        """confirma se realmente o usuário quer deletar o produto"""
        nome_removido = produto.nome
        session.delete(produto)
        session.commit()
        return f"Produto {nome_removido} (ID: {produto_id}) removido com sucesso."
    except Exception as e:
        session.rollback()
        return f'Erro ao deletar o produto. {str(e)}'
    finally:
        session.close

@tool
def cadastrar_cliente(nome: str, email: str):
    """Criar um novo cliente no banco de dados, usada quando o usuário pedir para cadastrar um novo cliente"""
    session = Session()
    try: 
        """ Usa os parâmetros passados (nome, email) e insere na tabela de clientes"""
        novo_cliente = Cliente(nome=nome, email=email)
        session.add(novo_cliente)
        session.commit()
        return f'O cliente {nome} foi cadastrado com sucesso!'
    
    except Exception as e:
        return f'Erro ao cadastrar o cliente. {str(e)}'
    
    finally:
        session.close()

@tool
def atualizar_cliente(cliente_id: int, novo_nome: str = None, novo_email: str = None):
    """Atualiza os dados nome e email de acordo com o que o usuário pediu para fazer, 
    usada quando o usuário pedir para atualizar os dados de algum cliente"""
    session = Session()
    try:
        cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            return f"Cliente com ID {cliente_id} não encontrado."
        
        if novo_nome: cliente.nome = novo_nome
        if novo_email: cliente.email = novo_email
        
        session.commit()
        return f"Dados do cliente {cliente_id} atualizados com sucesso."
    except Exception as e:
        session.rollback()
        return f'Erro ao criar o produto. {str(e)}'
    finally:
        session.close

@tool
def listar_clientes():
    """lista todos os clientes cadastrados, usada quando o usuário pedir para listar todos os clientes presentes na tabela Clientes"""
    session = Session()
    try:
        clientes = session.query(Cliente).all()
        if not clientes:
            return 'Nenhum cliente encontrado!'
        return '\n'.join([f'Nome: {c.nome}, Email: {c.email}' for c in clientes])
    finally:
        session.close()

"""Lista de tools para uso da llm"""
TOOLS: list[BaseTool] = [cadastrar_produto, atualizar_estoque, listar_produtos, 
                        deletar_produto, cadastrar_cliente, atualizar_cliente, listar_clientes]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}
