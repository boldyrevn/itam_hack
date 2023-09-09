from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.BigIntField(pk=True)
    student_email = fields.CharField(max_length=32, null=True, unique=True)
    login = fields.CharField(max_length=64, unique=True)
    hashed_password = fields.CharField(max_length=64)
    photo = fields.CharField(max_length=128, null=True)
    role = fields.CharField(max_length=32, null=True)
    team = fields.ForeignKeyField(
        model_name="models.Team",
        related_name="members",
        null=True,
        on_delete=fields.OnDelete.SET_NULL
    )
    cv = fields.TextField(null=True)
    academic_group = fields.CharField(max_length=32, null=True)

    def __str__(self):
        return self.login


class Team(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=32, unique=True)
    description = fields.TextField(null=True)
    captain_id = fields.IntField()

    def __str__(self):
        return self.name


class Hackathon(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=64)
    description = fields.TextField()
    contacts = fields.TextField()
    start_date = fields.DateField()
    end_date = fields.DateField()

    def __str__(self):
        return self.name


class Group(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=64, unique=True)
    team = fields.ForeignKeyField(model_name="models.Team", related_name="groups")
    hackathon = fields.ForeignKeyField(model_name="models.Hackathon", related_name="groups")
    status = fields.CharField(max_length=32)
    members = fields.ManyToManyField(model_name="models.User", related_name="groups")



