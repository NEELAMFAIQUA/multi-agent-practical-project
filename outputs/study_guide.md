# Study Group Guide: Photosynthesis

> Created by the offline Study Group Crew. All statements below are checked against the listed local evidence.

## Research brief

FACT: Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.
FACT: Water is absorbed by plant roots and transported to leaves.
FACT: Carbon dioxide enters leaves through small openings called stomata.
FACT: Chlorophyll is the green pigment in chloroplasts that absorbs light energy.
FACT: Photosynthesis takes place in chloroplasts in plant cells.

### Sources

- OpenStax Biology 2e, 8.1 Overview of Photosynthesis
- OpenStax Biology 2e, 8.2 The Light-Dependent Reactions of Photosynthesis

## Quiz and answer key

1. **Which two raw materials are converted during photosynthesis?**
   - Answer: carbon dioxide and water
   - Evidence: Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.
2. **Which two products are made during photosynthesis?**
   - Answer: glucose and oxygen
   - Evidence: Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.
3. **What pigment absorbs light energy in chloroplasts?**
   - Answer: chlorophyll
   - Evidence: Chlorophyll is the green pigment in chloroplasts that absorbs light energy.
4. **In which organelles in plant cells does photosynthesis take place?**
   - Answer: chloroplasts
   - Evidence: Photosynthesis takes place in chloroplasts in plant cells.

## Explanations

### Photosynthesis Inputs

Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen. Water is absorbed by plant roots and transported to leaves. Carbon dioxide enters leaves through small openings called stomata.

### Photosynthesis Outputs

Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.

### Chlorophyll

Chlorophyll is the green pigment in chloroplasts that absorbs light energy.

### Photosynthesis Location

Photosynthesis takes place in chloroplasts in plant cells.

## Fact-check

- **Photosynthesis Inputs** — answer: SUPPORTED: every sentence appears in the research evidence. Explanation: SUPPORTED: every sentence appears in the research evidence.
- **Photosynthesis Outputs** — answer: SUPPORTED: every sentence appears in the research evidence. Explanation: SUPPORTED: every sentence appears in the research evidence.
- **Chlorophyll** — answer: SUPPORTED: every sentence appears in the research evidence. Explanation: SUPPORTED: every sentence appears in the research evidence.
- **Photosynthesis Location** — answer: SUPPORTED: every sentence appears in the research evidence. Explanation: SUPPORTED: every sentence appears in the research evidence.

## Agent context flow

- `user topic` -> **Topic Researcher**; context: topic=photosynthesis; output: research_brief, citations, concepts.
- `Topic Researcher` -> **Quiz Maker**; context: research_brief and concepts; output: quiz with evidence-linked answer key.
- `Topic Researcher + Quiz Maker` -> **Explainer**; context: research_brief + quiz concepts and answers; output: plain-language explanations.
- `Topic Researcher + Quiz Maker + Explainer` -> **Fact-Checker**; context: research_brief + quiz + explanations; output: verified study guide.

## LangChain tool calls

- **Topic Researcher** invoked `search_study_sources` (retrieve source notes) with `topic=photosynthesis`.
- **Quiz Maker** invoked `build_practice_question` (build question) with `concept=photosynthesis inputs; source_notes=research brief (5 facts)`.
- **Quiz Maker** invoked `build_practice_question` (build question) with `concept=photosynthesis outputs; source_notes=research brief (5 facts)`.
- **Quiz Maker** invoked `build_practice_question` (build question) with `concept=chlorophyll; source_notes=research brief (5 facts)`.
- **Quiz Maker** invoked `build_practice_question` (build question) with `concept=photosynthesis location; source_notes=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify answer: photosynthesis inputs) with `claim=carbon dioxide and water; evidence=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify explanation: photosynthesis inputs) with `claim=Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen. Wat...; evidence=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify answer: photosynthesis outputs) with `claim=glucose and oxygen; evidence=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify explanation: photosynthesis outputs) with `claim=Photosynthesis uses light energy to convert carbon dioxide and water into glucose and oxygen.; evidence=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify answer: chlorophyll) with `claim=chlorophyll; evidence=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify explanation: chlorophyll) with `claim=Chlorophyll is the green pigment in chloroplasts that absorbs light energy.; evidence=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify answer: photosynthesis location) with `claim=chloroplasts; evidence=research brief (5 facts)`.
- **Fact-Checker** invoked `verify_claim` (verify explanation: photosynthesis location) with `claim=Photosynthesis takes place in chloroplasts in plant cells.; evidence=research brief (5 facts)`.
