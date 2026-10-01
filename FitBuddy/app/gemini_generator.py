from .gemini_client import generate_text
from .config import WORKOUT_MODEL

def generate_workout_gemini(user):
    prompt = f"""
You are FitBuddy, a careful fitness-planning assistant.
Create a personalized 7-day workout plan for:
Name: {user.username}
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Preferred intensity: {user.intensity}

Return exactly 7 clearly labelled days. For each day include:
- Focus
- Warm-up (5–10 minutes)
- Main workout with exercise names and sets/reps or duration
- Rest guidance
- Cooldown/recovery

Keep it practical for a general user. Include at least one recovery/rest-focused day.
Do not diagnose disease, prescribe medication, or claim guaranteed results.
If an exercise may be unsuitable for someone with an injury or medical condition,
tell the user to seek professional advice before doing it.
"""
    return generate_text(prompt, WORKOUT_MODEL)
