# AI Research Agent

**Jarvis** — an interactive command-line research assistant built with LangChain and Google's Gemini model. Ask it questions in a continuous session, and it uses web search and Wikipedia tools to gather information, returning a structured, nicely formatted summary each time — with the option to save findings to a file.

## What it does

1. Runs as an interactive loop — ask multiple research questions in one session without restarting the script
2. Uses an LLM-powered agent (Gemini `2.5-flash`) that can call tools as needed:
   - **Web search** (DuckDuckGo) for current, general information
   - **Wikipedia lookup** for background/reference information
   - **Save to file** to persist structured findings to `research_output.txt`
3. Parses the agent's final answer into a structured response with `topic`, `summary`, `source`, and `tools_used` fields, using Pydantic for validation
4. Displays results in a formatted [`rich`](https://github.com/Textualize/rich) panel plus a plain-text breakdown (topic, summary, sources, tools used), with a spinner shown while researching
5. Handles empty input, `exit`/`quit`/`q` commands, `Ctrl+C` interruption, and unexpected errors gracefully — the loop keeps running instead of crashing on a single bad query

## Requirements

- Python 3.9+
- A Google AI API key (for Gemini) — see [Google AI Studio](https://aistudio.google.com/) to get one

## Setup

1. Clone the repo:

```bash
git clone https://github.com/<your-username>/ai-research-agent.git
cd ai-research-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** rename `requirement.txt` to `requirements.txt` before publishing — `pip install -r requirements.txt` expects that exact filename by convention, and most people (and CI tools) won't think to look for anything else.

4. Create a `.env` file in the project root with your API key:

```
GOOGLE_API_KEY=your_key_here
```

5. Run the agent:

```bash
python main.py
```

6. Ask a research question at the prompt:

```
>>> Recent advances in solid-state batteries
```

Keep asking questions in the same session — type `exit`, `quit`, or `q` when you're done. Each query is researched independently (there's no memory of earlier questions in the session yet — see Limitations below).

The agent will search, reason about what it finds, and print a formatted panel plus a plain-text breakdown of the topic, summary, sources, and tools used. If it saves results, they'll be appended to `research_output.txt`.

## Project structure

```
.
├── main.py              # Entry point: sets up the LLM, prompt, and agent executor
├── tools.py              # Tool definitions: web search, Wikipedia, save-to-file
├── requirements.txt      # Python dependencies
└── research_output.txt   # Created automatically when the save tool is used
```

## How it works

- **`tools.py`** defines three LangChain `Tool` objects: a DuckDuckGo search wrapper, a Wikipedia query tool (limited to 1 result, 100 characters, to keep responses concise), and a file-saving utility that timestamps and appends research output.
- **`main.py`** builds a `ChatPromptTemplate` instructing the model to act as a research assistant and return output in a fixed format, defined by a Pydantic model (`ResearchResponse`). It creates a tool-calling agent via `create_tool_calling_agent` and runs it through an `AgentExecutor`.
- The `research()` function wraps a single query: it invokes the agent (showing a `rich` status spinner while it works), parses the raw output into the structured `ResearchResponse` model, and prints both a formatted panel and a plain-text breakdown. Since agent output format can vary (plain string vs. a list of content blocks), the parsing step handles both cases before validating with Pydantic.
- The main loop reads input continuously, handling `exit`/`quit`/`q`, blank input, `Ctrl+C`, and any other exception from `research()` without crashing the whole program — each is caught and reported, then the loop continues (except for a deliberate exit).

## Limitations & ideas for contribution

- No memory between queries — each question in a session is researched independently, with no awareness of earlier questions or answers (the `chat_history` placeholder in the prompt is never actually populated)
- Error handling is broad (a single `except Exception`) rather than specific — a missing API key, a network timeout, and a parsing failure all get the same generic message
- Wikipedia results are capped very short (100 characters) — may lose useful context on complex topics
- No test suite yet
- Could be extended with:
  - A simple web UI (Streamlit/Gradio) instead of terminal-only interaction
  - Support for additional LLM providers (the dependencies already include OpenAI/Anthropic LangChain integrations, unused so far)
  - Real conversation memory — actually populating `chat_history` so follow-up questions can reference earlier answers
  - Structured citation formatting instead of a flat source list
  - More specific error handling (e.g. a clear message when `GOOGLE_API_KEY` is missing, rather than surfacing whatever the SDK raises)
  - Unit tests for the tools and the output-parsing logic

## License

[MIT](LICENSE)
