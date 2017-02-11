from django.contrib.auth.models import User
from django.db import models
from food.models import School


class Profile(models.Model):
    user = models.OneToOneField(User)
    school = models.ForeignKey(School)
