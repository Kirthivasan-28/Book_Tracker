from fastapi import APIRouter, status, HTTPException
from app.database import db
from app.schemas.user import UserSignup, UserLogin
from app.auth.jwt_handler import hashPassword, verifyPassword, create_access_token
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
        inserted_id = str(result.inserted_id)
        return {
            "message":"User created Successfully!!",
            "email":create_user["email"],
            "id":inserted_id
        }
    except HTTPException:
        raise
    except (ConnectionError, TimeoutError) as e:
        raise HTTPException(status_code=500,detail="Database error while creating new entry")
    except Exception as e:
        print(f"Unexpected Error:{e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")



@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(userlogin: UserLogin):
    user_login = userlogin.model_dump()
    try:
        user_check = await db.user.find_one({"email":user_login["email"]})
        if not user_check:
            raise HTTPException(status_code = 401, detail = "Invalid email")
        if not verifyPassword(user_login["password"], user_check["password"]):
            raise HTTPException(status_code = 401, detail = "Invalid password")
        
        token = create_access_token({"sub":user_check["email"]})
        return {
            "access_token": token,
            "token_type":"bearer"
        }
    except HTTPException:
        raise 
    except Exception as e:
        print(f"Database error while login:{e}")
        raise HTTPException(status_code=500, detail = "Database error while fetching the user details!")