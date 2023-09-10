from typing import Optional
import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Table


class Base(DeclarativeBase):
    pass


user_group = Table(

)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_email: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(32), nullable=True)
    login: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(64))
    photo: Mapped[str] = mapped_column(String(32), nullable=True)
    cv: Mapped[Optional[str]]
    academic_group: Mapped[str] = mapped_column(String(32), nullable=True)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    team: Mapped[Optional["Team"]] = relationship(back_populates="members ")
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("role.id"))
    role: Mapped[Optional["Role"]] = relationship()

    def __str__(self):
        return self.name


class Team(Base):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=True)
    description: Mapped[Optional[str]]
    captain_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    captain: Mapped["User"] = relationship()
    members: Mapped[list["User"]] = relationship(back_populates="team")

    def __str__(self):
        return self.name


class Hackathon(Base):
    __tablename__ = "hackathon"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=True)
    description: Mapped[Optional[str]]
    contacts: Mapped[str]
    start_date: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]

    def __str__(self):
        return self.name


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    team: Mapped["Team"] = relationship()
    hackathon_id: Mapped[int] = mapped_column(ForeignKey("hackathon.id"))
    hackathon: Mapped["Hackathon"] = relationship()


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))


