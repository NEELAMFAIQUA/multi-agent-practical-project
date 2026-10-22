"""Local LangChain tools used by the Study Group Crew agents."""

from __future__ import annotations

import re

from langchain_core.tools import tool

_STUDY_CONTENT = {
    "photosynthesis": {
        "sources": [
            "Source: OpenStax Biology 2e, 8.1 Overview of Photosynthesis",
            "Source: OpenStax Biology 2e, 8.2 The Light-Dependent Reactions of Photosynthesis",
        ],
        "facts": [
            "Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.",
            "Water is absorbed by plant roots and transported to leaves.",
            "Carbon dioxide enters leaves through small openings called stomata.",
            "Chlorophyll is the green pigment in chloroplasts that absorbs light energy.",
            "Photosynthesis takes place in chloroplasts in plant cells.",
        ],
        "concepts": [
            "photosynthesis inputs",
            "photosynthesis outputs",
            "chlorophyll",
            "photosynthesis location",
        ],
    }
}

_QUESTION_BANK = {
    "photosynthesis inputs": (
        "Which two raw materials are converted during photosynthesis?",
        "carbon dioxide and water",
        "Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.",
    ),
    "photosynthesis outputs": (
        "Which two products are made during photosynthesis?",
        "glucose and oxygen",
        "Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.",
    ),
    "chlorophyll": (
        "What pigment absorbs light energy in chloroplasts?",
        "chlorophyll",
        "Chlorophyll is the green pigment in chloroplasts that absorbs light energy.",
    ),
    "photosynthesis location": (
        "In which organelles in plant cells does photosynthesis take place?",
        "chloroplasts",
        "Photosynthesis takes place in chloroplasts in plant cells.",
    ),
}


@tool
def search_study_sources(topic: str) -> str:
    """Retrieve curated factual notes, concepts, and citations for a study topic."""
    normalized = topic.strip().lower()
    if normalized not in _STUDY_CONTENT:
        available = ", ".join(sorted(_STUDY_CONTENT))
        raise ValueError(f"No local sources are configured for {topic!r}. Try: {available}.")
    content = _STUDY_CONTENT[normalized]
    lines = [*content["sources"]]
    lines.extend(f"FACT: {fact}" for fact in content["facts"])
    lines.extend(f"CONCEPT: {concept}" for concept in content["concepts"])
    return "\n".join(lines)


@tool
def build_practice_question(concept: str, source_notes: str) -> str:
    """Build one answerable question for a concept covered by the research notes."""
    if concept not in _QUESTION_BANK:
        raise ValueError(f"No question template is configured for {concept!r}.")
    question, answer, evidence = _QUESTION_BANK[concept]
    if evidence not in source_notes:
        raise ValueError(f"Research notes do not support the concept {concept!r}.")
    return f"question={question}\nanswer={answer}\nevidence={evidence}"


@tool
def verify_claim(claim: str, evidence: str) -> str:
    """Check that a claim is directly present in the supplied research evidence."""
    normalized_claims = [
        _normalize(sentence)
        for sentence in re.split(r"(?<=[.!?])\s+", claim.strip())
        if _normalize(sentence)
    ]
    normalized_evidence = _normalize(
        "\n".join(
            line.removeprefix("FACT: ").strip()
            for line in evidence.splitlines()
            if line.startswith("FACT: ") or not line.startswith(("Source:", "CONCEPT:"))
        )
    )
    if not normalized_claims:
        raise ValueError("Claim must not be empty.")
    unsupported = [sentence for sentence in normalized_claims if sentence not in normalized_evidence]
    if not unsupported:
        return "SUPPORTED: every sentence appears in the research evidence."
    return "UNSUPPORTED: one or more sentences were not found verbatim in the research evidence."


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
