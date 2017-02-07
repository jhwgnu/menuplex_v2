import requests, urllib.request
from bs4 import BeautifulSoup
from django.db import models
from datetime import datetime
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

    @staticmethod
    def printss():
        print("qwe")


class Meal(models.Model):
    school = models.ForeignKey(School,on_delete =models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete =models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=10,choices =TIME_CHOICES,default='lunch',)
    meal_date = models.DateField()

    def __str__(self):
        return self.name

    @classmethod
    def crawl_SNU(cls):
        today = datetime.now()
        snu = School.objects.get(name="서울대")

        def crawl_SNU_html(html):
            soup = BeautifulSoup(html, 'html.parser')
            snu_list1 = soup.select('.Content_bg table tbody tr')

            for restaurant in snu_list1[1:] :
                rest_name = restaurant.find('span').contents[0] # 식당 이름
                rest = Restaurant.objects.get(name=rest_name) # 식당 instance

                mornings = restaurant.select('td')[2].contents[0].replace('\xa0','').split('/')
                if mornings[0] !='': # 비어있지 않다면,
                    for morning in mornings :
                        cls.objects.create(school = snu , restaurant = rest, name = morning , time = "morning", meal_date = today)

                lunchs = restaurant.select('td')[4].contents[0].replace('\xa0','').split('/')
                if lunchs[0] !='': # 비어있지 않다면,
                    for lunch in lunchs :
                        cls.objects.create(school = snu , restaurant = rest, name = lunch , time = "lunch", meal_date = today)

                dinners = restaurant.select('td')[6].contents[0].replace('\xa0','').split('/')
                if dinners[0] !='': # 비어있지 않다면,
                    for dinner in dinners :
                        cls.objects.create(school = snu , restaurant = rest, name = dinner , time = "dinner", meal_date = today)

        # 크롤링을 했을 경우 동작하지 않도록함
        if not Meal.objects.filter(school=snu).filter(meal_date = datetime.now()):
            # 직영식당 크롤링
            html = urllib.request.urlopen("http://www.snuco.com/html/restaurant/restaurant_menu1.asp?date="+today.strftime("%Y-%m-%d"))
            crawl_SNU_html(html)
            # 위탁식당 크롤링
            html = urllib.request.urlopen("http://www.snuco.com/html/restaurant/restaurant_menu2.asp?date="+today.strftime("%Y-%m-%d"))
            crawl_SNU_html(html)


