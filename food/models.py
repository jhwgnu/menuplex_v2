from django.db import models

TIME_CHOICES = (
    ('morning', '조식'),
    ('lunch'  , '중식'),
    ('dinner' , '석식'),
)

class School(models.Model):
    name = models.CharField(max_length=100)
    school_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    school = models.ForeignKey(School,on_delete =models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meal(models.Model):
    school = models.ForeignKey(School,on_delete =models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete =models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=10,choices =TIME_CHOICES,default='lunch',)
    meal_date = models.DateField()
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name