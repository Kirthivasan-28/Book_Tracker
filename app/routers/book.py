from fastapi import APIRouter, status, HTTPException
from app.database import db
from app.schemas.book import BookCreate
from datetime import datetime, timezone

router = APIRouter()

@router.post("/add-book", status_code=status.HTTP_201_CREATED)
async def add_book(bookcreate: BookCreate):
    add_book = bookcreate.model_dump()
    add_book["added_at"] = datetime.now(timezone.utc)
    try: 
        existing_book = await db.book.find_one({"title":add_book["title"]})
        if existing_book:
            raise HTTPException(status_code=400, detail = "Book already exists in the registory!!")
        result = await db.book.insert_one(add_book)
        inserted_id = str(result.inserted_id)
        return {
            "message":"Book inserted successfully!!",
            "title":add_book["title"],
            "id":inserted_id
        }
    except HTTPException:
        raise
    except(ConnectionError, TimeoutError) as e:
        raise HTTPException(status_code=500,detail="Database error while creating new entry")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail = "An unexpected error occurred!")
    