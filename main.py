"""Run the Study Group Crew and write its study guide to disk."""

from pathlib import Path

from study_crew import run_crew

OUTPUT_FILE = Path(__file__).parent / "outputs" / "study_guide.md"


def render_markdown(result) -> str:
    lines = [
        f"# Study Group Guide: {result.topic.title()}",
        "",
        "> Created by the offline Study Group Crew. All statements below are checked against the listed local evidence.",
        "",
        "## Research brief",
        "",
        result.research_brief,
        "",
        "### Sources",
        "",
    ]
    lines.extend(f"- {citation.removeprefix('Source: ').strip()}" for citation in result.citations)
    lines.extend(["", "## Quiz and answer key", ""])
    for index, question in enumerate(result.quiz, start=1):
        lines.extend(
            [
                f"{index}. **{question['question']}**",
                f"   - Answer: {question['answer']}",
                f"   - Evidence: {question['evidence']}",
            ]
        )
    lines.extend(["", "## Explanations", ""])
    for concept, explanation in result.explanations.items():
        lines.extend([f"### {concept.title()}", "", explanation, ""])
    lines.extend(["## Fact-check", ""])
    for item in result.verification:
        lines.append(
            f"- **{item['concept'].title()}** — answer: {item['answer']} "
            f"Explanation: {item['explanation']}"
        )
    lines.extend(["", "## Agent context flow", ""])
    lines.extend(
        f"- `{link['from']}` -> **{link['to']}**; context: {link['context']}; "
        f"output: {link['artifact']}."
        for link in result.context_links
    )
    lines.extend(["", "## LangChain tool calls", ""])
    lines.extend(
        f"- **{call['agent']}** invoked `{call['tool']}` ({call['stage']}) "
        f"with `{call['input']}`."
        for call in result.tool_calls
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    result = run_crew()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(render_markdown(result), encoding="utf-8")
    print(f"Study guide saved to {OUTPUT_FILE.relative_to(Path(__file__).parent)}")
    print(f"Agents: 4 | LangChain tool calls: {len(result.tool_calls)}")


if __name__ == "__main__":
    main()
