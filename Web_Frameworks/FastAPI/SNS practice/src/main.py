from fastapi import FastAPI
from api import user, post, newsfeed, like, comment, follow

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(newsfeed.router)
app.include_router(like.router)
app.include_router(comment.router)
app.include_router(follow.router)
@app.get("/")
def health_check():
    return {"message": "Thread SNS API is running"}
