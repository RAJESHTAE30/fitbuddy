from .gemini_client import generate_text
from .config import TIP_MODEL

def generate_nutrition_tip_with_flash(goal):
    prompt = f"""
Give one concise, practical nutrition or recovery tip for a person whose fitness goal is "{goal}".
Keep it to 3–5 sentences. Mention a useful food/hydration/recovery habit and briefly explain why it helps.
Avoid extreme dieting, unsafe calorie restriction, supplement prescriptions, or medical claims.
"""
    return generate_text(prompt, TIP_MODEL)
