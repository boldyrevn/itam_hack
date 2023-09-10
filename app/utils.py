from app.models import User
from app.schemas import UserShow


def user_schema_from_orm(user: User) -> UserShow:
    return UserShow(
        login=user.login,
        id=user.id,
        photo=user.photo,
        name=user.name,
        role=user.role.name if user.role is not None else None,
        team=user.team.name if user.team is not None else None,
        cv=user.cv,
        academic_group=user.academic_group,
        student_email=user.student_email
    )



