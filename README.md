# Simple AI Research Agent
 
A simple command-line research assistant built with LangChain and Google's Gemini model. Give it a topic or question, and it uses web search and Wikipedia tools to gather information, then returns a structured summary — with the option to save findings to a file.
 
## What it does
 
1. Takes a research query from the user via terminal input
2. Uses an LLM-powered agent (Gemini `2.5-flash`) that can call tools as needed:
   - **Web search** (DuckDuckGo) for current, general information
   - **Wikipedia lookup** for background/reference information
   - **Save to file** to persist structured findings to `research_output.txt`
3. Parses the agent's final answer into a structured response with `topic`, `summary`, `source`, and `tools_used` fields, using Pydantic for validation
## Requirements
 
- Python 3.9+
- A Google AI API key (for Gemini) — see [Google AI Studio](https://aistudio.google.com/) to get one
Install dependencies:
 
```bash
pip install -r requirements.txt
```
 
## Setup
 
1. Clone the repo and install dependencies (above).
2. Create a `.env` file in the project root with your API key:
```
GOOGLE_API_KEY=your_key_here
```
 
3. Run the agent:
```bash
python main.py
```
 
4. When prompted, type your research question, e.g.:
```
What can I help you research? Recent advances in solid-state batteries
```
 
The agent will search, reason about what it finds, and print a structured summary. If you ask it to save the results, they'll be appended to `research_output.txt`.
 
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
- The raw agent output is parsed into the structured `ResearchResponse` model. Since agent output format can vary (plain string vs. a list of content blocks), the parsing step handles both cases before validating with Pydantic.
## Limitations & ideas for contribution
 
- Single-turn only — no conversation memory between queries in one run
- No error handling around missing/invalid API keys beyond what `dotenv`/the SDK raise natively
- Wikipedia results are capped very short (100 characters) — may lose useful context on complex topics
- No test suite yet
- Could be extended with:
  - A simple web UI (Streamlit/Gradio) instead of terminal-only interaction
  - Support for additional LLM providers (the dependencies already include OpenAI/Anthropic LangChain integrations, unused so far)
  - Conversation memory for follow-up questions
  - Structured citation formatting instead of a flat source list
  - Unit tests for the tools and the output-parsing logic
## License
 
[MIT](LICENSE)
