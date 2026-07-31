from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from tools import search_tool, wiki_tool, save_tool

from rich.console import Console
from rich.panel import Panel
import textwrap

# Load Environment Variables
load_dotenv()

# Console
console = Console()


# Output Schema
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = PydanticOutputParser(
    pydantic_object=ResearchResponse
)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a professional AI research assistant. Research the user's question using the available tools. Once you have enough information, return your answer ONLY in this format:

{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(
    format_instructions=parser.get_format_instructions()
)


# Tools
tools = [
    search_tool,
    wiki_tool,
    save_tool,
]

# Agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
)

# Research Function
def research(query: str):
    """Runs the research agent and displays the results."""

    with console.status("[bold green]Researching..."):
        raw_response = agent_executor.invoke({"query": query})

    output = raw_response.get("output")

    if isinstance(output, list):
        text = output[0]["text"]
    else:
        text = output

    structured_response = parser.parse(text)

    console.print(
        Panel(
            textwrap.fill(structured_response.summary, width=90),
            title=f" {structured_response.topic}",
            border_style="green",
        )
    )

    print("=" * 70)
    print(" RESEARCH RESULTS")
    print("=" * 70)

    print("\n Topic")
    print(f"{structured_response.topic}")

    print("\n Summary")
    print(textwrap.fill(structured_response.summary, width=90))

    print("\n Sources")
    for source in structured_response.source:
        print(f"• {source}")

    print("\n Tools Used")
    for tool in structured_response.tools_used:
        print(f"• {tool}")

    print("=" * 70)

# Main Program
console.print(
    Panel.fit(
        "[bold cyan]Hey, I am Jarvis, your personal AI Research Agent[/bold cyan]\n\n"
        "Ask me anything.\n"
        "Type [bold red]exit[/bold red] or [bold red]quit[/bold red] to leave.",
        border_style="cyan",
    )
)

while True:

    query = input("\n>>> ")

    if query.lower() in ["exit", "quit", "q"]:
        console.print("\n Goodbye! Have a great day.\n", style="bold green")
        break

    if not query.strip():
        console.print(" Please enter a research topic.", style="yellow")
        continue

    try:
        research(query)

    except KeyboardInterrupt:
        console.print("\n\n Program interrupted.", style="red")
        break

    except Exception as e:
        console.print(f"\n Error: {e}", style="bold red")