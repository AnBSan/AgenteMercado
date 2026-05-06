from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.state import RunnableConfig
from rich import print
from rich.markdown import Markdown
from rich.prompt import Prompt

from graph import build_graph
from prompt import SYSTEM_PROMPT


def main() -> None:
    graph = build_graph()
    config = RunnableConfig(configurable={"thread_id": 1})
    first_message = True

    prompt = Prompt()
    Prompt.prompt_suffix = ""

    print('\n[bold red]Bem vindo ao assistente de IA do mercado legal! Digite qual tipo de operação deseja ralizar (criar, listar, atualizar, ou deletar)\nPara sair digite: s ou sair')
    
    while True:
        user_input = prompt.ask("[bold cyan]Você: \n")
        print(Markdown("\n\n  ---  \n\n"))

        if user_input.lower() in ["q", "quit", "sair", "s", "exit", "e"]:
            print("[bold cyan]RESPOSTA: \n")
            print("Até mais 👋")
            break
        
        if first_message:
            messages = [SystemMessage(SYSTEM_PROMPT), HumanMessage(user_input)]
            first_message = False
        else:
            messages = [HumanMessage(user_input)]

        result = graph.invoke({"messages": messages}, config=config)

        print("[bold cyan]RESPOSTA: \n")
        print(Markdown(result["messages"][-1].content))
        print(Markdown("\n\n  ---  \n\n"))


if __name__ == "__main__":
    main()