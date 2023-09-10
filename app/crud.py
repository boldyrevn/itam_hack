from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app import models as m
from app.schemas import UserUpdate, GroupSchema, CreateTeam


def add_user(user: m.User, db: Session) -> None:
    db.add(user)
    db.commit()


def get_user(login, db: Session, *, full=False) -> m.User:
    if not full:
        stmt = select(m.User).where(m.User.login == login)
    else:
        stmt = select(m.User).where(m.User.login == login).options(
            joinedload(m.User.role), joinedload(m.User.team)
        )
    user = db.scalar(stmt)
    return user


def update_user(user: m.User, db: Session, new_data: UserUpdate) -> m.User:
    db.add(user)
    for field in new_data:
        if field[1] is not None:
            if field[0] != 'role':
                setattr(user, field[0], field[1])
            else:
                stmt = select(m.Role).where(m.Role.name == field[1])
                role = db.scalar(stmt)
                user.role = role
    db.commit()
    return user


def add_team(user: m.User, db: Session, team: CreateTeam) -> str:
    new_team = m.Team(name=team.name, description=team.description, captain_id=user.id)
    user.team = new_team
    db.add_all([new_team, user])
    db.commit()
    return new_team.name


def join_team(user: m.User, db: Session, team_name: str) -> str | None:
    stmt = select(m.Team).where(m.Team.name == team_name)
    team = db.scalar(stmt)
    if team is None:
        return None
    user.team = team
    db.add(user)
    db.commit()
    return team.name


