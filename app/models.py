from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.BigIntField(pk=True)
    student_email = fields.CharField(max_length=32, null=True, unique=True)
    login = fields.CharField(max_length=64, unique=True)
    hashed_password = fields.CharField(max_length=64)
    photo = fields.CharField(max_length=128, null=True)
    role = fields.CharField(max_length=32, null=True)
    team_id = fields.IntField(null=True)
    cv = fields.TextField(null=True)
    academic_group = fields.CharField(max_length=32, null=True)

    def __str__(self):
        return self.login


class Team(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=32)
    description = fields.TextField(null=True)
    captain_id = fields.IntField()
