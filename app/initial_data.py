from sqlalchemy.orm import Session
from app import crud
from app.schemas.user import UserCreate
from app.core.config import settings

def init_db(db: Session) -> None:
    # Create first superuser
    user = crud.user.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="Initial Admin",
            is_superuser=True,
            is_active=True,
        )
        user = crud.user.create(db, obj_in=user_in) 