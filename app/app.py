from typing import Annotated

from fastapi import FastAPI, HTTPException, status, Response, Depends, Cookie
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import crud
from app.models import User
from app.schemas import UserAuth, UserShow, CreateTeam, UserUpdate, JoinTeam, TeamShow
from app.utils import user_schema_from_orm
from config import settings
from database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


async def authenticate_user(login: str, password: str, db: Session) -> User | None:
    user = crud.get_user(login, db)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.hash_algorithm)
    return encoded_jwt


async def get_current_user(
        jwt_token: Annotated[str | None, Cookie()],
        db: Annotated[Session, Depends(get_db)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(jwt_token, settings.secret_key, settings.hash_algorithm)
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(login=login, db=db, full=True)
    if user is None:
        raise credentials_exception
    return user


@app.post("/login", response_model=UserShow)
async def login_for_access_token(user: UserAuth, response: Response, db: Annotated[Session, Depends(get_db)]):
    user = await authenticate_user(user.login, user.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.login})
    response.set_cookie(key="jwt_token", value=access_token)
    return UserShow(login=user.login, id=user.id)


@app.post('/register', response_model=UserShow)
async def create_user(user: UserAuth, db: Annotated[Session, Depends(get_db)]):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(login=user.login, hashed_password=hashed_password)
    try:
        crud.add_user(new_user, db)
        return UserShow(login=new_user.login, id=new_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with such login already exists"
        )


@app.get('/user_profile', response_model=UserShow)
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user_schema_from_orm(user)


@app.post('/user_profile', response_model=UserShow)
async def update_user(user: Annotated[User, Depends(get_current_user)],
                      upd_data: UserUpdate,
                      db: Annotated[Session, Depends(get_db)]):
    try:
        new_user = crud.update_user(user, db, upd_data)
        return user_schema_from_orm(new_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with such login already exists"
        )


@app.post('/create_team')
async def create_team(user: Annotated[User, Depends(get_current_user)],
                      team: CreateTeam,
                      db: Annotated[Session, Depends(get_db)]):
    if user.team is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already has a team")
    else:
        try:
            crud.add_team(user, db, team)
            return {"team": team.name}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Team with such name already exists")


@app.post('/join_team')
async def join_team(user: Annotated[User, Depends(get_current_user)],
                    team: JoinTeam,
                    db: Annotated[Session, Depends(get_db)]):
    if user.team is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already has a team")
    else:
        joined_team = crud.join_team(user, db, team.name)
        if joined_team is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="There is no team with such name")
        else:
            return {"team": joined_team}


@app.get('/user_team')
async def get_user_team(user: Annotated[User, Depends(get_current_user)],
                        db: Annotated[Session, Depends(get_db)]):
    if user.team is None:
        return None
    else:
        members = []
        for member in user.team.members:
            members.append(member.login)
        return TeamShow(name=user.team.name,
                        description=user.team.description,
                        members=members)
