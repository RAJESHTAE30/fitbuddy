from .gemini_client import generate_text
from .config import WORKOUT_MODEL

def update_workout_plan(original_plan, feedback, user):
    prompt = f"""
You are revising an existing FitBuddy 7-day workout plan.

User:
- Name: {user.username}
- Age: {user.age}
- Weight: {user.weight} kg
- Goal: {user.goal}
- Intensity: {user.intensity}

Original plan:
{original_plan}

User feedback:
{feedback}

Return a complete revised 7-day plan, not just the changed section.
Apply the feedback where it is reasonable, while preserving the user's goal and
appropriate recovery. Clearly label Day 1 through Day 7 and include focus,
warm-up, main workout, rest guidance, and cooldown/recovery.
Do not diagnose or prescribe medical treatment.
"""
    return generate_text(prompt, WORKOUT_MODEL)
