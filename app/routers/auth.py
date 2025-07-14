from fastapi import APIRouter, status, HTTPException
from database import db
from schemas.user import UserSignup
from auth.jwt_handler import hashPassword
from datetime import datetime, timezone
router = APIRouter()

@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def user_signup(usersignup: UserSignup):
    create_user= usersignup.model_dump()
    create_user["created_at"]= datetime.now(timezone.utc)
    create_user["password"]=hashPassword(create_user["password"])
    try:
        existing_user = await db.user.find_one({"email":create_user["email"]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered!")
        result = await db.user.insert_one(create_user)
        result["id"] = str(result.inserted_id)
        return {
            "message":"User created Successfully!!",
            "email":create_user["email"]
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail="Database error while creating new entry")
    