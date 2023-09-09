from pydantic import BaseModel


class UserAuth(BaseModel):
    login: str
    password: str | int
    # email: str = "bullshit"


class UserUpdate(BaseModel):
    id: int
    login: str
    photo: str | None = None
    role: str | None = None
    team_id: int | None = None
    cv: str | None = None
    academic_group: str | None = None
    student_email: str | None = None
