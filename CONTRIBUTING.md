# Contributing to AI Research Agent

Thanks for considering a contribution — this is a small project, so even modest improvements are meaningful.

## Ways to contribute

- **Fix a bug.** If the agent errors out on a particular kind of query, or the output parsing fails on a response shape it doesn't currently handle, that's a great first PR.
- **Add a tool.** New LangChain tools (e.g. an arXiv search, a news API, a calculator) following the pattern already established in `tools.py`.
- **Add LLM provider support.** The dependencies already include LangChain integrations for OpenAI and Anthropic that aren't wired up yet — adding a way to switch providers would be a valuable contribution.
- **Improve error handling.** Missing API keys, network failures, and malformed agent output currently aren't handled gracefully.
- **Add tests.** There's no test suite yet — unit tests for the tools in `tools.py` or the output-parsing logic in `main.py` are very welcome.

## Before you start

For anything beyond a small fix (a new tool, provider support, a UI), open an issue first to discuss the approach.

## Workflow

1. Fork the repository and create a branch from `main`:
   `git checkout -b feature/short-description`
2. Make your change.
3. Test it manually by running `python main.py` with a few different queries, including ones likely to hit edge cases (very short queries, queries needing multiple tool calls).
4. If you added a tool, document it in the README's "How it works" section.
5. Commit using the convention below and open a pull request.

## Coding standards

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- New tools should follow the existing pattern in `tools.py`: a plain function plus a `Tool(...)` wrapper with a clear `name` and `description` (the agent uses the description to decide when to call it, so be specific).
- Keep `.env`-based secrets out of commits — never hardcode API keys.

## Commit convention

```
<type>: <short summary>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

Example:

```
feat: add arXiv search tool
fix: handle missing GOOGLE_API_KEY with a clear error message
```

## Pull request checklist

- [ ] The change does one clear thing
- [ ] New tools include a clear `name` and `description`
- [ ] No API keys or secrets included in the diff
- [ ] README updated if behavior or setup steps changed
- [ ] Manually tested with at least one real query

## Code of conduct

Be respectful and constructive in issues and reviews. Disagreement about approach is fine; disrespect isn't.
