from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from .config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=False)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_user(user_data):
    with SessionLocal() as db:
        existing = db.query(User).filter(User.user_id == user_data.user_id).first()
        if existing:
            existing.username = user_data.username
            existing.age = user_data.age
            existing.weight = user_data.weight
            existing.goal = user_data.goal
            existing.intensity = user_data.intensity
            db.commit()
            return existing.id
        user = User(
            user_id=user_data.user_id, username=user_data.username,
            age=user_data.age, weight=user_data.weight,
            goal=user_data.goal, intensity=user_data.intensity
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id

def save_plan(user_id, original_plan, nutrition_tip):
    with SessionLocal() as db:
        plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan.id

def get_original_plan(user_id):
    with SessionLocal() as db:
        plan = db.query(Plan).filter(Plan.user_id == user_id).order_by(Plan.id.desc()).first()
        return plan

def update_plan(user_id, updated_plan, feedback):
    with SessionLocal() as db:
        plan = db.query(Plan).filter(Plan.user_id == user_id).order_by(Plan.id.desc()).first()
        if not plan:
            return None
        plan.updated_plan = updated_plan
        plan.feedback = feedback
        plan.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(plan)
        return plan

def get_all_users():
    with SessionLocal() as db:
        return db.query(User).order_by(User.id.desc()).all()

def get_all_plans():
    with SessionLocal() as db:
        return db.query(Plan).order_by(Plan.id.desc()).all()

def delete_user(user_id):
    with SessionLocal() as db:
        db.query(Plan).filter(Plan.user_id == user_id).delete()
        db.query(User).filter(User.user_id == user_id).delete()
        db.commit()
