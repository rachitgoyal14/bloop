import json
from app.services.llm_service import LLMService
from app.core.prompts.teach_ai_prompt import build_teach_ai_prompt
from app.services.learning_context_service import load_learning_context


class TeachAIService:
    def __init__(self):
        self.llm = LLMService()

    def evaluate(self, concept_id: str, explanation: str, level: str) -> dict:
        context = load_learning_context(concept_id)

        prompt = build_teach_ai_prompt(
            concept=context["concept_name"],
            learning_goals=context["learning_goals"],
            explanation=explanation,
            level=level
        )

        response = self.llm.complete(prompt)

        try:
            result = json.loads(response)
        except Exception:
            raise ValueError("LLM returned invalid JSON")

        scores = result.get("scores", {})
        feedback = result.get("feedback", [])
        follow_up = result.get("follow_up_question")

        max_score = len(context["learning_goals"]) * 2
        achieved = sum(scores.values())

        return {
            "scores": scores,
            "feedback": feedback,
            "follow_up_question": follow_up,
            "passed": achieved / max_score >= 0.7
        }
