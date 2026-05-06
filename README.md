# Documentação do Projeto: AgenteMercado

## 1. Introdução

O projeto `AgenteMercado` é um assistente de IA desenvolvido para gerenciar operações de um mercado, incluindo cadastro e atualização de produtos e clientes. Ele utiliza a biblioteca LangGraph para orquestrar um fluxo de trabalho conversacional, onde um Large Language Model (LLM) interage com o usuário e executa ações específicas através de ferramentas (tools) que manipulam um banco de dados SQLite.

## 2. Arquitetura Geral

A arquitetura do sistema é baseada em um grafo de estados (StateGraph) gerenciado pelo LangGraph. O fluxo principal envolve a interação do usuário com o LLM, que, por sua vez, pode invocar ferramentas para interagir com um banco de dados. O estado da conversação é mantido através de mensagens que transitam pelo grafo.

Os principais componentes são:

*   **`main.py`**: Ponto de entrada da aplicação, responsável pela interface com o usuário e execução do grafo.
*   **`graph.py`**: Define a estrutura do grafo de estados, incluindo os nós (`call_llm`, `tool_node`) e a lógica de roteamento (`router`).
*   **`tools.py`**: Contém as funções (tools) que o LLM pode invocar para realizar operações no banco de dados.
*   **`tables.py`**: Define o esquema do banco de dados (tabelas `Produtos` e `Clientes`) usando SQLAlchemy.
*   **`prompt.py`**: Armazena o prompt do sistema que guia o comportamento do LLM.
*   **`state.py`**: Define a estrutura do estado que é passado entre os nós do grafo.
*   **`utils.py`**: Funções utilitárias para carregar o modelo de linguagem (LLM).

## 3. Componentes Detalhados

### 3.1. `main.py`

Este arquivo é o ponto de entrada da aplicação. Ele inicializa o grafo de estados e entra em um loop de interação com o usuário. As mensagens do usuário são passadas para o grafo, e as respostas do LLM são exibidas. O `SYSTEM_PROMPT` é injetado na primeira interação para configurar o comportamento do LLM.

### 3.2. `graph.py`

O coração da orquestração do agente. Define um `StateGraph` com os seguintes nós e lógica:

*   **`call_llm`**: Este nó é responsável por invocar o LLM. Ele recebe o estado atual (que contém as mensagens da conversa) e retorna a resposta do LLM, que pode ser uma mensagem de texto ou uma chamada de ferramenta.
*   **`tool_node`**: Este nó é ativado quando o LLM decide usar uma ferramenta. Ele extrai os detalhes da chamada da ferramenta da resposta do LLM, executa a ferramenta correspondente e retorna o resultado da execução da ferramenta como uma `ToolMessage`.
*   **`router`**: Uma função de roteamento que decide o próximo nó a ser executado com base na resposta do LLM. Se a resposta do LLM contiver uma chamada de ferramenta, o roteador direciona para `tool_node`; caso contrário, a conversa é encerrada (`__end__`).

O grafo é construído com as seguintes transições:

*   `START` -> `call_llm`
*   `call_llm` -> `tool_node` (se o LLM chamar uma ferramenta)
*   `call_llm` -> `__end__` (se o LLM não chamar uma ferramenta)
*   `tool_node` -> `call_llm` (após a execução de uma ferramenta, o LLM é chamado novamente para processar o resultado)

### 3.3. `tools.py`

Este arquivo define as ferramentas que o LLM pode utilizar para interagir com o banco de dados. Cada função decorada com `@tool` representa uma ferramenta, com uma docstring que descreve sua finalidade e parâmetros. As ferramentas disponíveis são:

*   **`cadastrar_produto(nome: str, preco: float, quantidade: int = 0)`**: Adiciona um novo produto à tabela `Produtos`.
*   **`atualizar_estoque(produto_id: int, nova_quantidade: int)`**: Atualiza a quantidade em estoque de um produto existente.
*   **`listar_produtos()`**: Retorna uma lista formatada de todos os produtos cadastrados.
*   **`deletar_produto(produto_id: int)`**: Remove um produto da tabela `Produtos`.
*   **`cadastrar_cliente(nome: str, email: str)`**: Adiciona um novo cliente à tabela `Clientes`.
*   **`atualizar_cliente(cliente_id: int, novo_nome: str = None, novo_email: str = None)`**: Atualiza o nome e/ou email de um cliente existente.
*   **`listar_clientes()`**: Retorna uma lista formatada de todos os clientes cadastrados.

### 3.4. `tables.py`

Define o modelo de dados para o banco de dados SQLite `mercado_legal.db` usando SQLAlchemy. As classes `Produto` e `Cliente` representam as tabelas no banco de dados, com seus respectivos campos e tipos de dados.

*   **`Produto`**: Representa a tabela `Produtos` com `id`, `nome`, `preco` e `quantidade`.
*   **`Cliente`**: Representa a tabela `Cliente` com `id`, `nome` e `email`.

O arquivo também configura o `engine` e a `Session` para interação com o banco de dados. Quando executado diretamente, ele cria o arquivo `mercado_legal.db` e as tabelas se elas não existirem.

### 3.5. `prompt.py`

Contém a constante `SYSTEM_PROMPT`, que é uma string multilinha em português. Este prompt é crucial para guiar o comportamento do LLM, instruindo-o sobre seu papel como assistente de gerenciamento de estoque/clientes, as regras de interação (análise de intenção, uso obrigatório de ferramentas para ações no DB, solicitação de campos ausentes, feedback conciso e confirmação antes de exclusões) e a lista de ferramentas disponíveis. Ele também especifica que as respostas devem ser em português brasileiro e em tom profissional.

### 3.6. `state.py`

Define a estrutura do estado (`State`) que é utilizada pelo LangGraph. Atualmente, o estado consiste em uma sequência de mensagens (`messages`), que acumula o histórico da conversação e as interações com as ferramentas. A anotação `Annotated[Sequence[BaseMessage], add_messages]` indica que novas mensagens são adicionadas ao final da sequência.

### 3.7. `utils.py`

Fornece funções para carregar o modelo de linguagem. Atualmente, inclui `load_llm_ollama()`, que inicializa um modelo Ollama (`ollama:llama3.2:latest`). Este arquivo é responsável por abstrair a configuração do LLM, permitindo fácil troca de modelos ou provedores.

## 4. Configuração e Dependências

O projeto requer as seguintes dependências, listadas no arquivo `requirements.txt`:

*   `langchain`
*   `langgraph`
*   `sqlalchemy`
*   `langchain-ollama`
*   `rich`

Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```

Além disso, é necessário ter um servidor Ollama em execução com o modelo `llama3.2:latest` disponível, ou configurar as variáveis de ambiente para outros provedores de LLM, conforme a implementação em `utils.py`.

## 5. Como Executar

1.  Certifique-se de ter o Python 3.x instalado.
2.  Instale as dependências listadas em `requirements.txt`.
3.  (Opcional, mas recomendado) Configure um servidor Ollama e baixe o modelo `llama3.2:latest`.
4.  Execute o arquivo `main.py`:

    ```bash
    python main.py
    ```

5.  Interaja com o assistente de IA através do terminal.

## 6. Conclusão

O `AgenteMercado` é um exemplo robusto de como combinar LLMs com ferramentas e um grafo de estados para criar assistentes conversacionais capazes de interagir com sistemas externos, como bancos de dados. A modularidade do design permite fácil extensão e manutenção das funcionalidades de gerenciamento de produtos e clientes.
