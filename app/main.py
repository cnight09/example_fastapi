from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, config
from .database import engine
from .routers import post, user, auth, vote

#creates tables as needed
# models.Base.metadata.create_all(bind=engine)

# goes through functions/code/decorators below and finds/uses the first one to match the path used in the call (order of decorators/functions matter)
# request method, url: "/"
app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

#manual list of posts and fuctions to retreive them
#my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1, "published": False, "rating": 1}
#,{"title": "title of post 2", "content": "content of post 2", "id": 2, "published": True} ]

#def find_post(id):
#    for p in my_posts:
#        if p["id"] == id:
#            return p

#def find_index_post(id):
#    for i, p in enumerate(my_posts):
#        if p["id"] == id:
#            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# path operation
# @app.get("/") - is a @/decorator for a path operation for FastAPI
# app is the FastAPI object created above
# get is the CRUD HTTP method
# "/" is the path (which is empty in this case so, the root path)
@app.get("/")
# function - called root (keep names as descriptive as possible)
# async - is setting this up as an asynchronous call
async def root():
# data sent back to caller as a python dictionary converted to JSON format via FastAPI
  #  return {"message": "Hello World"}
    return {"message": "Welcome to my API!!"}