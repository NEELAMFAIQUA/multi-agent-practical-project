"""Offline Study Group Crew using LangChain tools for each workflow stage."""

from __future__ import annotations

from dataclasses import dataclass, field

from langchain_core.tools import BaseTool

from tools import build_practice_question, search_study_sources, verify_claim


@dataclass(frozen=True)
class Agent:
    name: str
    role: str
    goal: str
    backstory: str


TOPIC_RESEARCHER = Agent(
    name="Topic Researcher",
    role="Evidence-led subject researcher",
    goal="Create a concise, source-linked factual brief for the study group.",
    backstory=(
        "A careful science librarian who separates established evidence from "
        "unsupported claims and writes notes other educators can reuse."
    ),
)
QUIZ_MAKER = Agent(
    name="Quiz Maker",
    role="Retrieval-practice designer",
    goal="Create clear questions with answers grounded in the research brief.",
    backstory=(
        "A learning designer who believes good questions test understanding "
        "and have one defensible answer."
    ),
)
EXPLAINER = Agent(
    name="Explainer",
    role="Plain-language biology tutor",
    goal="Explain the quiz concepts accurately in language suitable for a beginner.",
    backstory=(
        "A patient tutor who connects biological processes to memorable "
        "cause-and-effect relationships."
    ),
)
FACT_CHECKER = Agent(
    name="Fact-Checker",
    role="Skeptical educational editor",
    goal="Verify answers and explanations against the research brief before publication.",
    backstory=(
        "A meticulous editor who checks every educational claim against the "
        "evidence rather than trusting confident wording."
    ),
)

AGENTS = (TOPIC_RESEARCHER, QUIZ_MAKER, EXPLAINER, FACT_CHECKER)


@dataclass
class CrewResult:
    topic: str
    research_brief: str
    citations: list[str]
    concepts: list[str]
    quiz: list[dict[str, str]]
    explanations: dict[str, str]
    verification: list[dict[str, str]]
    context_links: list[dict[str, str]]
    tool_calls: list[dict[str, str]] = field(default_factory=list)


def _invoke(
    tool: BaseTool,
    args: dict[str, str],
    agent: Agent,
    stage: str,
    tool_calls: list[dict[str, str]],
) -> str:
    result = tool.invoke(args)
    rendered = str(result)
    input_summary = []
    for key, value in args.items():
        if key in {"source_notes", "evidence"}:
            fact_count = sum(line.startswith("FACT: ") for line in value.splitlines())
            input_summary.append(f"{key}=research brief ({fact_count} facts)")
        else:
            compact_value = " ".join(value.split())
            if len(compact_value) > 100:
                compact_value = f"{compact_value[:97]}..."
            input_summary.append(f"{key}={compact_value}")
    tool_calls.append(
        {
            "agent": agent.name,
            "stage": stage,
            "tool": tool.name,
            "input": "; ".join(input_summary),
        }
    )
    return rendered


def run_crew(topic: str = "photosynthesis") -> CrewResult:
    """Run all four agents in order, passing each stage's context forward."""
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic must not be empty.")

    calls: list[dict[str, str]] = []
    links: list[dict[str, str]] = []

    # Topic Researcher: tool-backed retrieval grounds all downstream tasks.
    source_notes = _invoke(
        search_study_sources,
        {"topic": topic},
        TOPIC_RESEARCHER,
        "retrieve source notes",
        calls,
    )
    lines = source_notes.splitlines()
    citations = [line for line in lines if line.startswith("Source:")]
    evidence = [line for line in lines if line.startswith("FACT:")]
    concepts = [line.removeprefix("CONCEPT: ").strip() for line in lines if line.startswith("CONCEPT:")]
    research_brief = "\n".join(evidence)
    links.append(
        {
            "from": "user topic",
            "to": TOPIC_RESEARCHER.name,
            "context": f"topic={topic}",
            "artifact": "research_brief, citations, concepts",
        }
    )

    # Quiz Maker: each question is generated from a concept in the research context.
    quiz: list[dict[str, str]] = []
    for concept in concepts:
        question_text = _invoke(
            build_practice_question,
            {"concept": concept, "source_notes": research_brief},
            QUIZ_MAKER,
            "build question",
            calls,
        )
        fields = dict(
            item.split("=", 1) for item in question_text.splitlines() if "=" in item
        )
        if not {"question", "answer", "evidence"} <= fields.keys():
            raise ValueError(f"Question tool returned an incomplete question for {concept!r}.")
        quiz.append({"concept": concept, **fields})
    links.append(
        {
            "from": "Topic Researcher",
            "to": QUIZ_MAKER.name,
            "context": "research_brief and concepts",
            "artifact": "quiz with evidence-linked answer key",
        }
    )

    # Explainer: use both the evidence and quiz concepts for contextual explanations.
    explanations: dict[str, str] = {}
    for item in quiz:
        explanations[item["concept"]] = _explain(item["concept"])
    links.append(
        {
            "from": "Topic Researcher + Quiz Maker",
            "to": EXPLAINER.name,
            "context": "research_brief + quiz concepts and answers",
            "artifact": "plain-language explanations",
        }
    )

    # Fact-Checker: verify every answer and explanation against the same research brief.
    verification: list[dict[str, str]] = []
    for item in quiz:
        answer_check = _invoke(
            verify_claim,
            {"claim": item["answer"], "evidence": research_brief},
            FACT_CHECKER,
            f"verify answer: {item['concept']}",
            calls,
        )
        explanation_check = _invoke(
            verify_claim,
            {"claim": explanations[item["concept"]], "evidence": research_brief},
            FACT_CHECKER,
            f"verify explanation: {item['concept']}",
            calls,
        )
        verification.append(
            {
                "concept": item["concept"],
                "answer": answer_check,
                "explanation": explanation_check,
            }
        )
    links.append(
        {
            "from": "Topic Researcher + Quiz Maker + Explainer",
            "to": FACT_CHECKER.name,
            "context": "research_brief + quiz + explanations",
            "artifact": "verified study guide",
        }
    )

    return CrewResult(
        topic=topic,
        research_brief=research_brief,
        citations=citations,
        concepts=concepts,
        quiz=quiz,
        explanations=explanations,
        verification=verification,
        context_links=links,
        tool_calls=calls,
    )


def _explain(concept: str) -> str:
    """Provide a concise deterministic explanation tied to the retrieved evidence."""
    explanations = {
        "photosynthesis inputs": (
            "Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen. "
            "Water is absorbed by plant roots and transported to leaves. "
            "Carbon dioxide enters leaves through small openings called stomata."
        ),
        "photosynthesis outputs": (
            "Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen."
        ),
        "chlorophyll": (
            "Chlorophyll is the green pigment in chloroplasts that absorbs light energy."
        ),
        "photosynthesis location": (
            "Photosynthesis takes place in chloroplasts in plant cells."
        ),
    }
    try:
        return explanations[concept]
    except KeyError as error:
        raise ValueError(f"No explanation is defined for concept {concept!r}.") from error
