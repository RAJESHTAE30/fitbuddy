from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .schemas import UserInput, FeedbackRequest
from .database import (
    save_user, save_plan, get_original_plan, update_plan,
    get_all_users, get_all_plans, delete_user, SessionLocal, User
)
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan
from .config import ADMIN_USERNAME, ADMIN_PASSWORD

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

def render_error(request, message, status_code=400):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"message": message},
        status_code=status_code
    )

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        user = UserInput(
            username=username, user_id=user_id, age=age,
            weight=weight, goal=goal, intensity=intensity
        )
        save_user(user)
        workout_plan = generate_workout_gemini(user)
        nutrition_tip = generate_nutrition_tip_with_flash(user.goal)
        save_plan(user.user_id, workout_plan, nutrition_tip)
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "updated": False,
                "message": None
            }
        )
    except ValueError as exc:
        return render_error(request, str(exc))
    except Exception as exc:
        return render_error(request, f"Could not generate the plan. {exc}", 500)

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):
    try:
        feedback_data = FeedbackRequest(user_id=user_id, feedback=feedback)
        plan = get_original_plan(feedback_data.user_id)
        if not plan:
            return render_error(request, "No plan was found for that User ID.", 404)

        with SessionLocal() as db:
            user = db.query(User).filter(User.user_id == feedback_data.user_id).first()
            if not user:
                return render_error(request, "User was not found.", 404)

        revised = update_workout_plan(plan.updated_plan or plan.original_plan, feedback_data.feedback, user)
        update_plan(feedback_data.user_id, revised, feedback_data.feedback)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": revised,
                "nutrition_tip": plan.nutrition_tip,
                "updated": True,
                "message": "Your workout plan has been updated using your feedback."
            }
        )
    except ValueError as exc:
        return render_error(request, str(exc))
    except Exception as exc:
        return render_error(request, f"Could not update the plan. {exc}", 500)

@router.get("/admin", response_class=HTMLResponse)
def admin_login(request: Request):
    return templates.TemplateResponse(request=request, name="admin_login.html", context={})

@router.post("/admin", response_class=HTMLResponse)
def admin_auth(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        return templates.TemplateResponse(
            request=request,
            name="admin_login.html",
            context={"error": "Invalid admin credentials."},
            status_code=401
        )
    return RedirectResponse("/view-all-users", status_code=303)

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    users = get_all_users()
    plans = get_all_plans()
    plans_by_user = {}
    for plan in plans:
        plans_by_user.setdefault(plan.user_id, []).append(plan)
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users, "plans_by_user": plans_by_user}
    )

@router.post("/admin/delete/{user_id}")
def admin_delete_user(user_id: str):
    delete_user(user_id)
    return RedirectResponse("/view-all-users", status_code=303)

@router.get("/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}
