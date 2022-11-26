import uvicorn
from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import post, user, auth, vote

models.BaseEntity.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)