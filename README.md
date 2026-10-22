# Study Group Crew

A small, runnable multi-agent study group for **photosynthesis**. Four role-defined agents research a topic, build a quiz, explain the concepts, and check the result. The crew runs locally without an API key; the agents use deterministic instructional logic and actual LangChain tools, not a remote language model.

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt`

## Run

```powershell
python -m pip install -r requirements.txt
python main.py
```

The generated study guide is saved to `outputs/study_guide.md`. Running the program again refreshes the sample output.

Run the tests with:

```powershell
python -m unittest discover -s tests -v
```

## Agents and information flow

| Agent | Role, goal, and backstory | Receives | Produces |
|---|---|---|---|
| **Topic Researcher** | A careful science librarian who turns trusted source notes into a concise, evidence-linked brief. Goal: give the crew a factual foundation. | Topic | Research brief, citations, and key concepts |
| **Quiz Maker** | A retrieval-practice designer who writes clear questions with unambiguous answers. Goal: help learners test understanding, not just recall vocabulary. | Research brief | Questions and answer key |
| **Explainer** | A patient biology tutor who connects processes with plain-language explanations. Goal: make each quiz concept understandable. | Research brief and quiz | Concept explanations |
| **Fact-Checker** | A skeptical editor who checks every answer and explanation against the brief. Goal: flag unsupported or incorrect claims before publication. | Research brief, quiz, and explanations | Verification results and approved guide |

The context links are implemented in `crew.py` and displayed in the generated guide:

```text
Topic -> Topic Researcher -> research_brief
research_brief -> Quiz Maker -> quiz
research_brief + quiz -> Explainer -> explanations
research_brief + quiz + explanations -> Fact-Checker -> verified guide
```

## LangChain tools

`tools.py` defines three tools with LangChain's `@tool` decorator. They are invoked via `.invoke()` in the relevant agents: `search_study_sources` retrieves the local evidence notes for the researcher, `build_practice_question` builds a question for the quiz maker, and `verify_claim` checks quiz answers and explanations for the fact-checker. Their calls and context inputs are recorded in `CrewResult.tool_calls`.

This offline demo uses curated local evidence and fixed instructional logic. It does **not** call an LLM or claim that an LLM generated or independently validated the content. To use a model-backed version, an LLM would need to be added and configured separately.

## Reflection

See [`REFLECTION.md`](REFLECTION.md) for the project reflection.
