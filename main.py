from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base, UpdateUser

app = FastAPI()
engine = create_engine('postgresql://fastapi:fastapi@localhost/fastapi_db')
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


@app.post('/users/')
async def create_user(user: dict):
    db = SessionLocal()
    db_user = User(name=user['name'], age=user['age'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'status': 'User created successfully'}


@app.get('/users/')
async def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    return {'users': users}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    print(user_id)
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {'message': 'User deleted successfully'}


@app.put('/users/{user_id}')
async def put_user(user_id: int, user: UpdateUser):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    return {'message': 'User updated successfully'}
