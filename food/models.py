import requests, urllib.request, collections, functools, re
from django.core.urlresolvers import reverse
from bs4 import BeautifulSoup
from django.db import models
from datetime import datetime
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings


TIME_CHOICES = (
    ('morning', '조식'),
    ('lunch'  , '중식'),
    ('dinner' , '석식'),
)


#날짜를 기준으로 동일 날짜에 한번 연산을 햇으면
# 메모아이징 시켜서 또 연산 하는 것을 방지해줌
def memoize(f):
    memo = {}
    def helper(cls,x):
        t = datetime.today().day
        if (x,t) not in memo:
            if f(cls,x):
                memo[(x,t)] = f(cls,x)
        return memo[(x,t)]
    return helper

def memoize1(f):
    memo = {}
    def helper(x):
        t = datetime.today().day
        if (x,t) not in memo:
            if f(x):
                memo[(x,t)] = f(x)
        return memo[(x,t)]
    return helper

def memoize_check(f):
    memo = {}
    t = datetime.today().day
    def helper(cls,x, check):
        if check :
            if f(cls,x):
                memo[(x,t)] = f(cls,x)
            return memo[(x,t)]
        else :
            if (x,t) not in memo:
                if f(cls,x):
                    memo[(x,t)] = f(cls,x)
            return memo[(x,t)]
    return helper

class School(models.Model):
    name = models.CharField(max_length=100)
    school_url = models.URLField(max_length=200)
    shortname = models.CharField(max_length=10)
    logo = models.ImageField()

    def __str__(self):
        return self.name

    # views.py에서 레스토랑의 이름 - 시간 - 식사 이름 을 출력해주는 창.
    @classmethod
    @memoize_check
    def detail_list(cls,school_id,check=False):
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

    @classmethod
    def kakaotalk_list(cls,name):
        school = School.objects.get(name = name)
        return "" + name + "\n-----------------------\n" + Restaurant.kakaotalk_rest_list(school)
def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid LngLat Type')



class Restaurant(models.Model):
    school = models.ForeignKey(School,on_delete =models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("food:restaurant", args=[self.school.shortname, self.name])

    class Meta:
        ordering = ['-id']

    @classmethod
    @memoize
    def kakaotalk_rest_list(cls,school):
        result = ""
        today = datetime.now()
        for restaurant in Restaurant.objects.filter(school = school):
            meal_list = Meal.objects.filter(restaurant = restaurant).filter(meal_date = today)
            result += "[" + restaurant.name +"]\n"
            if meal_list :
                #조식 리스트
                meal_time_list = meal_list.filter(time = "morning")
                if  meal_time_list:
                    result += "    (조식)\n"
                    for meal in meal_time_list:
                        result += "    >"+ meal.name + "\n"
                else :
                    result += "    (조식) : 제공하지 않습니다 ㅠㅠ\n"
                #중식 리스트
                meal_time_list = meal_list.filter(time = "lunch")
                if meal_time_list :
                    result += "    (중식)\n"
                    for meal in meal_time_list:
                        result += "    >"+ meal.name + "\n"
                else :
                    result += "    (중식) : 제공하지 않습니다 ㅠㅠ\n"
                #석식 리스트
                meal_time_list = meal_list.filter(time = "dinner")
                if meal_time_list:
                    result += "    (석식)\n"
                    for meal in meal_time_list:
                        result += "    >"+ meal.name + "\n"
                else :
                    result += "    (석식) : 제공하지 않습니다 ㅠㅠ\n"
                # 줄바꿈

            else :
                result += "오늘 식사가 없습니다 ㅠㅠ\n"
            result += "\n"+"\n"
        return result

class Comment(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-id']



class Meal(models.Model):
    school = models.ForeignKey(School,on_delete =models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete =models.CASCADE)
    name = models.CharField(max_length=800)
    time = models.CharField(max_length=10,choices =TIME_CHOICES,default='lunch',)
    meal_date = models.DateField()
    soldout = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    # 메뉴의 히스토리를 가져오는 것
    # 같은 식당에 한에서만 가져와야 함.
    @memoize1
    def history(meal_id):
        h_meal = Meal.objects.get(pk=meal_id)
        return Meal.objects.filter(name = h_meal.name).filter(restaurant = h_meal.restaurant).filter(time = h_meal.time)

    # 학교 별로 묶어놓은 크롤러
    # admin에서 이용하기 위함
    @classmethod
    def crawl_SCHOOL(cls, queryset):
        for query in queryset :
            if (query == School.objects.get(name="서울대")) :
                cls.crawl_SNU()
            elif (query == School.objects.get(name="고려대")) :
                cls.crawl_KU()
            elif (query == School.objects.get(name="한양대")) :
                cls.crawl_HYU()

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
                        cls.objects.get_or_create(school = snu , restaurant = rest, name = morning , time = "morning", meal_date = today)

                lunchs = restaurant.select('td')[4].contents[0].replace('\xa0','').split('/')
                if lunchs[0] !='': # 비어있지 않다면,
                    for lunch in lunchs :
                        cls.objects.get_or_create(school = snu , restaurant = rest, name = lunch , time = "lunch", meal_date = today)

                dinners = restaurant.select('td')[6].contents[0].replace('\xa0','').split('/')
                if dinners[0] !='': # 비어있지 않다면,
                    for dinner in dinners :
                        cls.objects.get_or_create(school = snu , restaurant = rest, name = dinner , time = "dinner", meal_date = today)

        # 크롤링을 했을 경우 동작하지 않도록함
        if not Meal.objects.filter(school=snu).filter(meal_date = datetime.now()):
            # 직영식당 크롤링
            html = urllib.request.urlopen("http://www.snuco.com/html/restaurant/restaurant_menu1.asp?date="+today.strftime("%Y-%m-%d"))
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
                                if '-' in menu.select("p")[i].string:
                                    m_list = menu.select("p")[i].string.split('-') # 0번째 원소 : 식사 시간 // 1번째 원소 : 음식 이름
                                    cls.objects.get_or_create(school = ku, restaurant = rest, name = m_list[1],time = date_change(m_list[0]), meal_date = t_date)
                                elif ':' in menu.select("p")[i].string:
                                    m_list = menu.select("p")[i].string.split(':') # 0번째 원소 : 식사 시간 // 1번째 원소 : 음식 이름
                                    cls.objects.get_or_create(school = ku, restaurant = rest, name = m_list[1],time = 'lunch', meal_date = t_date)
                                else :
                                    cls.objects.get_or_create(school = ku, restaurant = rest, name = menu.select("p")[i].string ,time = 'lunch', meal_date = t_date)
                        else : # 메뉴가 1개인 식당
                            cls.objects.get_or_create(school = ku , restaurant = rest, name = menu.next.string , time = "lunch", meal_date = t_date)

    # 한양대 대상으로 한 크롤러
    @classmethod
    def crawl_HYU(cls):
        hyu =  School.objects.get(name="한양대")
        today = datetime.now()
        # url 별로 식당이 잡혀 있기 때문에 새로히 메소드 정의해줌
        def crawl_HYU_url(url,rest) :
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')

            table = soup.find('tbody').find_next('tbody')
            if(url == "http://www.hanyang.ac.kr/web/www/-250#none"):
                table = soup.find('tbody').find_next('tbody').find_next('tbody')
            flour_food = "" # 분식은 일단 중식으로 넣자
            breakfast = ""
            lunch = ""
            dinner = ""

            try:
                tr = table.find('tr')
                td = tr.find('td').find_next('td')
                ul = td.find('ul')
                li = ul.find_all('li')

                for li_tag in li:
                    if len(li_tag) > 0:
                        if flour_food == "":
                            flour_food = li_tag.string
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="lunch",meal_date=today)
                        else:
                            flour_food += (", "+li_tag.string)
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="lunch",meal_date=today)

            except AttributeError:
                pass
            except IndexError:
                pass

            try:
                tr = table.find('tr').find_next('tr')
                td = tr.find('td').find_next('td')
                ul = td.find('ul')
                li = ul.find_all('li')

                for li_tag in li:
                    if len(li_tag) > 0:
                        if breakfast == "":
                            breakfast = li_tag.string
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="morning",meal_date=today)
                        else:
                            breakfast += (", "+li_tag.string)
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="morning",meal_date=today)
            except AttributeError:
                pass
            except IndexError:
                pass

            try:
                tr = table.find('tr').find_next('tr').find_next('tr')
                td = tr.find('td').find_next('td')
                ul = td.find('ul')
                li = ul.find_all('li')

                for li_tag in li:
                    if len(li_tag) > 0:
                        if lunch == "":
                            lunch = li_tag.string
                            cls.objects.create(school=hyu, restaurant=rest, name=li_tag.string, time="lunch", meal_date=today)
                        else:
                            lunch += (", "+li_tag.string)
                            cls.objects.create(school=hyu, restaurant=rest, name=li_tag.string, time="lunch", meal_date=today)
            except AttributeError:
                pass
            except IndexError:
                pass

            try:
                tr = table.find('tr').find_next('tr').find_next('tr').find_next('tr')
                td = tr.find('td').find_next('td')
                ul = td.find('ul')
                li = ul.find_all('li')

                for li_tag in li:
                    if len(li_tag) > 0:
                        if breakfast == "":
                            breakfast = li_tag.string
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="morning",meal_date=today)
                        else:
                            breakfast += (", "+li_tag.string)
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="morning",meal_date=today)
                        if lunch == "":
                            lunch = li_tag.string
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="lunch",meal_date=today)
                        else:
                            lunch += (", "+li_tag.string)
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="lunch",meal_date=today)
            except AttributeError:
                pass
            except IndexError:
                pass

            try:
                tr = table.find('tr').find_next('tr').find_next('tr').find_next('tr').find_next('tr')
                td = tr.find('td').find_next('td')
                ul = td.find('ul')
                li = ul.find_all('li')

                for li_tag in li:
                    if len(li_tag) > 0:
                        if dinner == "":
                            dinner = li_tag.string
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="dinner",meal_date=today)
                        else:
                            dinner += (", "+li_tag.string)
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="dinner",meal_date=today)
            except AttributeError:
                pass
            except IndexError:
                pass

            try:
                tr = table.find('tr').find_next('tr').find_next('tr').find_next('tr').find_next('tr').find_next('tr')
                td = tr.find('td').find_next('td')
                ul = td.find('ul')
                li = ul.find_all('li')

                for li_tag in li:
                    if len(li_tag) > 0:
                        if lunch == "":
                            lunch = li_tag.string
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="lunch",meal_date=today)
                        else:
                            lunch += (", "+li_tag.string)
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="lunch",meal_date=today)
                        if dinner == "":
                            dinner = li_tag.string
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="dinner",meal_date=today)
                        else:
                            dinner += (", "+li_tag.string)
                            cls.objects.get_or_create(school=hyu,restaurant=rest, name = li_tag.string,time="dinner",meal_date=today)
            except AttributeError:
                pass
            except IndexError:
                pass

        # 이미 그 날자의 크롤링이 존재하는 경우, 동작하지 않도록함
        if not Meal.objects.filter(school=hyu).filter(meal_date = datetime.now()):
            #학생 식당
            rest = Restaurant.objects.get(name = "학생식당")
            crawl_HYU_url("http://www.hanyang.ac.kr/web/www/-248#none",rest)

            #교직원 식당
            rest = Restaurant.objects.get(name = "교직원식당")
            crawl_HYU_url("http://www.hanyang.ac.kr/web/www/-249#none",rest)

            #사랑방
            rest = Restaurant.objects.get(name = "사랑방")
            crawl_HYU_url("http://www.hanyang.ac.kr/web/www/-250#none",rest)

            #신교직원식당
            rest = Restaurant.objects.get(name = "신교직원식당")
            crawl_HYU_url("http://www.hanyang.ac.kr/web/www/-251#none",rest)

            #신학생식당
            rest = Restaurant.objects.get(name = "신학생식당")
            crawl_HYU_url("http://www.hanyang.ac.kr/web/www/-252#none",rest)

            #제2생활관 식당
            rest = Restaurant.objects.get(name = "제2생활관식당")
            crawl_HYU_url("http://www.hanyang.ac.kr/web/www/-2-#none",rest)

            #행원파크
            rest = Restaurant.objects.get(name = "행원파크")
            crawl_HYU_url("http://www.hanyang.ac.kr/web/www/-253#none",rest)


class Map(models.Model):
    user = models.ForeignKey(User)
    school = models.ForeignKey(School)
    rest_name = models.ForeignKey(Restaurant)
    # 학교랑 관련된 식당만 받으려고 삽질하다가 실패! ㅎㅎㅎㅎㅎ
    # rest_name = Restaurant.objects.filter(school=school)
    lnglat = models.CharField(max_length=50, blank=True,
            validators=[lnglat_validator])

class Mealcomment(models.Model):
    meal = models.ForeignKey(Meal)
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-id']
