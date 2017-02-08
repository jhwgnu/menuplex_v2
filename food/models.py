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

    # views.py에서 레스토랑의 이름 - 시간 - 식사 이름 을 출력해주는 창.
    # cashing을 이용해서 한번 계산하면 저장해버리고, 다음 호출 시 걍 줄 수 있도록 하자.
    @classmethod
    def detail_list(cls,school_id):
        restaurant_list = Restaurant.objects.filter(school_id=school_id)
        meal_list = Meal.objects.filter(school_id=school_id).filter(meal_date=datetime.now())

        grouped_rest=dict()
        for obj in meal_list.all():
            name = restaurant_list.get(pk=obj.restaurant_id).name
            grouped_rest.setdefault((name,obj.time),[]).append(obj)

        grouped_time = dict()
        for key, value in grouped_rest.items():
            name = key[0]
            grouped_time.setdefault(name,[]).append((key[1],value))

        restaurant_dict = grouped_time.items()
        return restaurant_dict

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


    # 서울대 대상한 크롤러
    # 식당이 없었을 경우, 식당의 정보를 입력해주는 크롤러 제작 필요
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
            html = urllib.req0uest.urlopen("http://www.snuco.com/html/restaurant/restaurant_menu1.asp?date="+today.strftime("%Y-%m-%d"))
            crawl_SNU_html(html)
            # 위탁식당 크롤링
            html = urllib.request.urlopen("http://www.snuco.com/html/restaurant/restaurant_menu2.asp?date="+today.strftime("%Y-%m-%d"))
            crawl_SNU_html(html)


    # 고려대 대상한 크롤러
    @classmethod
    def crawl_KU(cls):
        def date_change(date): # 조식 중식 등으로 저장된 크롤링 값을 lunch / dinner 로 바꾸어줌
            if ("중식" or "점심") in date:
                return "lunch"
            elif ("석식" or "저녁") in date:
                return "dinner"
            elif ("조식" or "아침") in date:
                return "morning"
            else :
                return "lunch" # 샐러드 바 같은 것은 일단 중식으로 처리

        ku = School.objects.get(name="고려대")
        Year = str(datetime.now().year)

        # 이미 그 날자의 크롤링이 존재하는 경우, 동작하지 않도록함
        if not Meal.objects.filter(school=ku).filter(meal_date = datetime.now()):

            html = urllib.request.urlopen("http://www.korea.ac.kr/user/restaurantMenuAllList.do?siteId=university")
            soup = BeautifulSoup(html, 'html.parser')

            for index in range(0,len(soup.select(".ku_restaurant ul li"))) :

                x = soup.select(".ku_restaurant ul li")[index] # 식당 별로 쪼개기

                if x.div and x.div.strong != None :
                    rest_name = x.div.strong.string # 식당 이름
                    rest = Restaurant.objects.get(name=rest_name)

                else :
                    if x.span :
                        mon = x.find_all("span",class_="date")[0].contents[1].string
                        day = x.find_all("span",class_="date")[0].contents[3].string
                        t_date = datetime.strptime(Year+" "+mon+" "+day,"%Y %m %d")

                        menu = x.select(".menulist")[0]

                        if menu.select("p"):
                            for i in range(0,len(menu.select("p"))): # 메뉴가 1개보다 많은 식당
                                m_list = menu.select("p")[i].string.split('-') # 0번째 원소 : 식사 시간 // 1번째 원소 : 음식 이름
                                cls.objects.create(school = ku, restaurant = rest, name = m_list[1],time = date_change(m_list[0]), meal_date = t_date)
                        else : # 메뉴가 1개인 식당
                            cls.objects.create(school = ku , restaurant = rest, name = menu.next.string , time = "lunch", meal_date = t_date)


