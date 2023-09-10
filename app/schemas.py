from pydantic import BaseModel


class UserAuth(BaseModel):
    login: str
    password: str | int
    # email: str = "bullshit"


class UserShow(BaseModel):
    id: int
    name: str | None = None
    login: str
    photo: str | None = None
    role: str | None = None
    team: str | None = None
    cv: str | None = None
    academic_group: str | None = None
    student_email: str | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    photo: str | None = None
    role: str | None = None
    cv: str | None = None
    academic_group: str | None = None
    student_email: str | None = None


class GroupSchema(BaseModel):
    name: str
    hackathon: str
    members: list[str]


class CreateTeam(BaseModel):
    name: str
    description: str | None = None


class JoinTeam(BaseModel):
    name: str


class TeamShow(BaseModel):
    name: str
    description: str | None = None
    members: list[str]
