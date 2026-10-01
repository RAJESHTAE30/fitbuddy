from pydantic import BaseModel, Field, field_validator

ALLOWED_GOALS = {"weight loss", "muscle gain", "general wellness", "flexibility", "fitness"}
ALLOWED_INTENSITIES = {"low", "medium", "high"}

class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=120)
    user_id: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=500)
    goal: str = Field(min_length=2, max_length=100)
    intensity: str

    @field_validator("username", "user_id")
    @classmethod
    def clean_text(cls, value):
        return value.strip()

    @field_validator("goal")
    @classmethod
    def normalize_goal(cls, value):
        value = value.strip().lower()
        return value

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value):
        value = value.strip().lower()
        if value not in ALLOWED_INTENSITIES:
            raise ValueError("Intensity must be low, medium, or high.")
        return value

class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=100)
    feedback: str = Field(min_length=3, max_length=2000)
