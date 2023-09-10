from typing import Annotated

import tortoise
from fastapi import FastAPI, HTTPException, status, Response, Depends, Cookie
from jose import jwt, JWTError
from passlib.context import CryptContext
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError

from app.tortoise_models import User, Team
from app.schemas import UserAuth, UserUpdate, GroupSchema, CreateTeam
from config import settings
from old_database import TORTOISE_ORM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


async def authenticate_user(login: str, password: str) -> User | None:
    user = await User.get_or_none(login=login)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def user_schema_from_tortoise(user: User) -> UserUpdate:
    if user.team is None:
        team = None
    else:
        team = user.team.name
    roles = []
    for role in user.roles:
        roles.append(role)
    return UserUpdate(
        login=user.login,
        id=user.id,
        photo=user.photo,
        name=user.name,
        roles=roles,
        team=team,
        cv=user.cv,
        academic_group=user.academic_group,
        student_email=user.student_email
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.hash_algorithm)
    return encoded_jwt


async def get_current_user(jwt_token: Annotated[str | None, Cookie()]) -> User:
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
    user = await User.get_or_none(login=login)
    if user is None:
        raise credentials_exception
    await user.fetch_related("team", "roles")
    return user


@app.post("/login", response_model=UserUpdate)
async def login_for_access_token(user: UserAuth, response: Response):
    user = await authenticate_user(user.login, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.login})
    response.set_cookie(key="jwt_token", value=access_token)
    return UserUpdate(login=user.login, id=user.id)


@app.post('/register', response_model=UserUpdate)
async def create_user(user: UserAuth):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(login=user.login, hashed_password=hashed_password)
    try:
        await new_user.save()
        return UserUpdate(login=new_user.login, id=new_user.id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )


@app.get('/user_profile', response_model=UserUpdate)
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user_schema_from_tortoise(user)


@app.get('/user_groups', response_model=list[GroupSchema])
async def get_user_groups(user: Annotated[User, Depends(get_current_user)]):
    db_user = await User.get(id=user.id)
    await db_user.fetch_related('groups')
    groups = []
    for group in db_user.groups:
        await group.fetch_related('members')
        new_group = dict()
        new_group['name'] = group.name
        new_group['members'] = []
        for member in group.members:
            new_group['members'].append(member.name)
        groups.append(new_group)
    return groups


@app.post('/create_team')
async def create_team(user: Annotated[User, Depends(get_current_user)], team: CreateTeam):
    if user.team is not None:
        pass
    else:
        try:
            new_team = Team(name=team.name, description=team.description, captain_id=user.id)
            user.team = new_team
            # await new_team.save()
            await user.team.save()
            tortoise.fields.relational._NoneAwaitable
            user._
            user = await User.get(id=user.id)
            print(type(user.team))
            print(user.team)
            return {'team': new_team.name}
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team with such name already exists"
            )


register_tortoise(
    app=app,
    config=TORTOISE_ORM
)
