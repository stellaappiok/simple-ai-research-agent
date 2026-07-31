# LEARN.md

A guide to what this project teaches, for anyone studying it to learn agentic AI development.

## Who this is for

- Anyone who understands basic Python and has used an LLM API directly (a single prompt/response call) but hasn't yet built something that calls tools or returns structured output
- Students exploring LangChain specifically, or agent frameworks in general

## Prerequisites

- Comfortable with Python functions, classes, and basic async/sync API calls
- Some exposure to what an LLM API call looks like (even just using ChatGPT/Gemini's web UI conceptually)
- A free Google AI Studio API key to actually run it

## Core concepts this project demonstrates

### 1. Tool-calling agents
Rather than a single prompt-in, text-out call, this project shows an LLM deciding *which* tool to use (web search, Wikipedia, or save-to-file) based on the query, and *when* to stop and answer. Read `tools.py` first, then trace how `create_tool_calling_agent` in `main.py` wires those tools to the model.

### 2. Structured output with Pydantic
LLMs return free text by default. The `ResearchResponse` Pydantic model plus `PydanticOutputParser` show one common pattern for forcing a model's output into a predictable, validated shape (`topic`, `summary`, `source`, `tools_used`) that downstream code can rely on.

### 3. Prompt templates with format instructions
Look at how `parser.get_format_instructions()` gets injected into the system prompt via `.partial()`. This is the mechanism that tells the model *how* to structure its final answer so the parser can actually parse it.

### 4. Agent executors
`AgentExecutor` is the loop that actually runs the agent: call the model, check if it wants to use a tool, run the tool, feed the result back, repeat until the model produces a final answer. Setting `verbose=True` (as this project does) is the fastest way to actually *see* that loop happening — run it once with verbose output before changing anything.

### 5. Handling inconsistent LLM output formats
The `try`/`except` block in `main.py` handles the fact that agent output isn't always a plain string — sometimes it's a list of content blocks. This is a real, common gotcha when working with different model providers through LangChain, not a hypothetical edge case.

## Suggested way to study this repo

1. Run it once as-is with a simple query and read the `verbose=True` output closely — watch the agent decide to search, then decide to look something up on Wikipedia, then decide it has enough to answer.
2. Read `tools.py` end to end — it's short and each tool follows the same shape (a function + a `Tool` wrapper).
3. Read `main.py` top to bottom, matching each piece (the Pydantic model, the prompt template, the agent, the executor) to what you observed in step 1.
4. Break something on purpose: comment out `wiki_tool` from the `tools` list and see how the agent's behavior and output change.
5. Extend it: add a new tool (see `CONTRIBUTING.md`) — this is the fastest way to confirm you actually understand how the pieces connect.

## Common points of confusion

- **"Why does the model need format instructions in the prompt if we're using a Pydantic parser?"** The parser only validates output *after* the model responds — it can't force the model to respond in that shape. The format instructions in the prompt are what actually guides the model to produce parseable text in the first place.
- **"Why does `AgentExecutor` need both the agent and the tools passed to it separately?"** The agent decides *what* to call; the executor is what actually *has* the tools and can run them. Separating "decide" from "execute" is a recurring pattern in agent frameworks worth recognizing elsewhere.

## Where to go next

- Try swapping `ChatGoogleGenerativeAI` for `ChatOpenAI` or `ChatAnthropic` (both already in `requirements.txt`) to see how little of the agent logic needs to change when swapping providers.
- Look into LangChain's memory modules to add multi-turn conversation support.
- Explore LangGraph (LangChain's newer agent-orchestration library) once this pattern feels solid — it's the natural next step for more complex, multi-step agent workflows.

## License

[MIT](LICENSE)
