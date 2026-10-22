import unittest

from langchain_core.tools import BaseTool

from main import render_markdown
from study_crew import AGENTS, run_crew
from tools import build_practice_question, search_study_sources, verify_claim


class StudyCrewTests(unittest.TestCase):
    def test_four_agents_have_meaningful_definitions(self):
        self.assertEqual(len(AGENTS), 4)
        for agent in AGENTS:
            with self.subTest(agent=agent.name):
                self.assertTrue(agent.role)
                self.assertTrue(agent.goal)
                self.assertTrue(agent.backstory)

    def test_langchain_tools_are_used_and_all_claims_pass(self):
        self.assertTrue(all(isinstance(tool, BaseTool) for tool in (
            search_study_sources,
            build_practice_question,
            verify_claim,
        )))
        result = run_crew()
        self.assertEqual(
            {call["tool"] for call in result.tool_calls},
            {search_study_sources.name, build_practice_question.name, verify_claim.name},
        )
        self.assertEqual(len(result.quiz), 4)
        self.assertTrue(
            all(
                check.startswith("SUPPORTED")
                for item in result.verification
                for check in (item["answer"], item["explanation"])
            )
        )

    def test_information_flow_and_output_rendering(self):
        result = run_crew()
        self.assertEqual(len(result.context_links), 4)
        guide = render_markdown(result)
        for agent in ("Topic Researcher", "Quiz Maker", "Explainer", "Fact-Checker"):
            self.assertIn(agent, guide)
        self.assertIn("LangChain tool calls", guide)
        self.assertIn("Agent context flow", guide)
        self.assertIn("OpenStax Biology 2e", guide)

    def test_unknown_topic_fails_explicitly(self):
        with self.assertRaises(ValueError):
            run_crew("unknown topic")


if __name__ == "__main__":
    unittest.main()
