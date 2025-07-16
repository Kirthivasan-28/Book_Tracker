from fastapi import FastAPI
from app.routers import auth, book

app = FastAPI()
app.include_router(auth.router)
app.include_router(book.router)