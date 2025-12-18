def build_teach_ai_prompt(
    concept: str,
    learning_goals: list,
    explanation: str,
    level: str
) -> str:
    goals = "\n".join([f"- {g}" for g in learning_goals])

    level = level.lower()

    if level == "beginner":
        level_rules = """
Learner level: BEGINNER

Evaluation rules:
- Use simple, intuitive language
- Do NOT expect formal definitions
- Do NOT penalize lack of technical terms
- Focus on whether the core idea is understood
"""
    elif level == "intermediate":
        level_rules = """
Learner level: INTERMEDIATE

Evaluation rules:
- Expect correct terminology
- Expect clear structure in explanation
- Penalize vague or incomplete reasoning
- Focus on conceptual correctness
"""
    else:  # advanced
        level_rules = """
Learner level: ADVANCED

Evaluation rules:
- Expect precise and formal explanations
- Penalize oversimplification
- Expect mention of edge cases or limitations
- Focus on rigor and completeness
"""

    return f"""
You are evaluating a learner teaching an AI a concept.

Concept: {concept}

{level_rules}

Learning goals:
{goals}

User explanation:
\"\"\"{explanation}\"\"\"

Scoring instructions:
For each learning goal, score:
0 = missing or incorrect
1 = partially correct
2 = clearly and correctly explained

Important:
- Be strict according to the learner level.
- Do NOT provide hints or teaching.
- ONLY evaluate the learner's explanation.

Return JSON ONLY in this format:
{{
  "scores": {{
    "goal_1": 0,
    "goal_2": 2
  }},
  "feedback": [
    "short, specific feedback sentence"
  ],
  "follow_up_question": "single question testing the weakest learning goal"
}}
"""
