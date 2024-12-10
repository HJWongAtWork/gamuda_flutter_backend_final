from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.schemas import UserResponse
from app.models.database import User
from app.api.dependencies import get_current_user

router = APIRouter(tags=["Users"])

@router.post("/users/all", response_model=List[UserResponse])
async def get_users(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all users."""
    try:
        users = db.query(User).all()
        return [
            UserResponse(
                id=user.id,
                name=user.name,
                age=user.age,
                city=user.city,
                salary=user.salary,
                join_date=user.join_date.isoformat()
            )
            for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
