from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
#ver1
#def get_posts():
    # logic to retreive all posts
#    return {"data": "This is your posts"}
#ver2
#def get_posts():
#    return{"data": my_posts}
#ver3 - using direct connection
#def get_posts():
#    cursor.execute("""SELECT * FROM posts """)
#    posts = cursor.fetchall()
#    print(posts)
#    return {"data": posts}
#ver4 - using orm (sqlalchemy)
#query parameters are listed as agruments in the function (ex: limit, skip, search)
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):
# all posts
#   posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
# only posts for the current user
#    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

#default sql alchemy join is left inner join, to add vote count
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


# path parameter get request by id
#@router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
#ver1
#def get_post(id: int, response: Response):
#    post = find_post(id)
#    if not post:
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return{"message": f"post with id: {id} was not found"}
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"post with id: {id} was not found")
#    return{"post_detail": post}
#ver2 - using direct connection
#def get_post(id: int):
#    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
#    post = cursor.fetchone()
#    if post == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"post with id: {id} was not found")
#    return {"data": post}
#ver3 - orm (sqlalchemy)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#    post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
#    if post.owner_id != current_user.id:
#        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
#ver1
#def create_posts(payload: dict = Body(...)):
#    print(payload)
#    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
#ver2
#def create_posts(post: Post):
# logic to create a post
#    print(post)
# converts the pydantic model to a python dictionary .dict()
#    post_dict = post.dict()
#    post_dict['id'] = randrange(0,1000000)
#    my_posts.append(post_dict)
#    return {"data": post_dict}
# title str, content str, published bool
#ver3 - using direct connection
#def create_posts(post: Post):
#    cursor.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING * """,
#                    (post.title, post.content, post.published, post.rating))
#    new_post = cursor.fetchone()
#    conn.commit()
#    return {"data": new_post}
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
#   new_post = models.Post(title=post.title, content=post.content, published=post.published, rating=post.rating)
#    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
#ver1
#def delete_post(id: int, response: Response):
# logic to delete a post
# find the index in the array with the required id
#    index = find_index_post(id)
#    if index == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"post with id {id} does not exist")

#    my_posts.pop(index)
#    return {"message": "post was successfully deleted"}
# if error with length to long due to 204 use return below
#    return Response(status_code=status.HTTP_204_NO_CONTENT)
#ver2 - using direct connection
#def delete_post(id: int, response: Response):
#    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
#    deleted_post = cursor.fetchone()
#    if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id {id} does not exist")
#    conn.commit()
#    return {"message": deleted_post}
#ver3 - orm (sqlalchemy)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()   
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
#ver1
#def update_post(id: int, post: Post):
#    index = find_index_post(id)
#    if index == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                    detail=f"post with id {id} does not exist")

#    post_dict = post.dict()
#    post_dict['id'] = id
#    my_posts[index] = post_dict
#    print(post)
#    return {"data": my_posts[index]}
#ver2 - using direct connection
#def update_post(id: int, post: Post):
#    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING * """,
#                (post.title, post.content, post.published, post.rating, str(id)))
#    updated_post = cursor.fetchone()
#    if updated_post == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"post with id {id} does not exist")    
#    conn.commit()
#    return {"data": updated_post}
#ver3 - orm (sqlalchemy)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()   
    return post_query.first()