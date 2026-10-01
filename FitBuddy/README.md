# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite web application based on the supplied project documentation. It uses Google's Gemini API to generate personalized 7-day workout plans, concise nutrition/recovery tips, and feedback-based plan updates.

## Features

- User form: name, user ID, age, weight, fitness goal, intensity
- AI-generated 7-day workout plan
- Nutrition/recovery tip
- Feedback-based workout regeneration
- SQLite + SQLAlchemy persistence
- Admin login and user/plan dashboard
- Original and updated plans retained
- FastAPI interactive API docs
- Responsive HTML/CSS interface
- Environment variables for API credentials

## 1. Requirements

- Python 3.10+
- VS Code
- Internet connection for Gemini API calls
- A Google Gemini API key

## 2. Create virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env`:

```cmd
copy .env.example .env
```

Open `.env` and replace:

```env
GEMINI_API_KEY=your_real_key_here
```

Do not commit `.env` to Git.

## 5. Start the app

```bash
uvicorn app.main:app --reload
```

Open:

- App: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Admin: http://127.0.0.1:8000/admin

Default local admin credentials:

```text
Username: admin
Password: fitbuddy123
```

Change them in `.env` for anything beyond local testing.

## 6. Test the application

1. Open the home page.
2. Enter a test user such as:
   - Name: Harini
   - User ID: FB001
   - Age: 20
   - Weight: 55
   - Goal: Muscle Gain
   - Intensity: Medium
3. Click Generate My 7-Day Plan.
4. Confirm the workout and nutrition tip appear.
5. Submit feedback such as `Add more cardio and one extra recovery day`.
6. Confirm the revised 7-day plan appears.
7. Open `/admin` and log in.
8. Confirm the original and updated plans are visible.
9. Open `/docs` and test `/health`.

## 7. Automated smoke tests

Install dependencies, then run:

```bash
pytest
```

The tests verify application startup, the home route, health route, and admin page rendering without making a Gemini API request.

## Architecture

```text
Browser
   |
   v
FastAPI routes.py
   |--------> Jinja2 templates
   |
   +--------> Gemini client
   |             |--> workout generation
   |             |--> nutrition tip
   |             +--> feedback update
   |
   +--------> SQLAlchemy
                 |
                 v
             SQLite DB
```

## Important implementation note

The supplied documentation names Gemini 1.5 Pro and Gemini Flash and uses the older `google-generativeai` package. This implementation uses Google's current `google-genai` SDK and configurable modern model names so the project is maintainable. The architecture and user-facing functionality remain the same.

FitBuddy gives general fitness/wellness information and is not a substitute for professional medical advice.
