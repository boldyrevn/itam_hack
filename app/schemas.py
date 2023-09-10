from pydantic import BaseModel


class UserAuth(BaseModel):
    login: str
    password: str | int
    # email: str = "bullshit"


class UserUpdate(BaseModel):
    id: int
    name: str | None = None
    login: str
    photo: str | None = None
    roles: list[str] | None = None
    team: str | None = None
    cv: str | None = None
    academic_group: str | None = None
    student_email: str | None = None


class GroupSchema(BaseModel):
    name: str
    members: list[str]


class CreateTeam(BaseModel):
    name: str
    description: str | None = None
