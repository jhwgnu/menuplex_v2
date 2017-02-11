from django.contrib.auth.models import User
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(User)
    school = models.CharField(max_length = 10, blank = False)


