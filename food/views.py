from django.shortcuts import render
from django.http import HttpResponse
from food.models import School, Restaurant, Meal
from datetime import datetime
# Create your views here.
def index(request):
    school_list = School.objects.all()
    context = {'school_list': school_list}

    return render(request, 'food/index.html',context)


def detail(request,school_id):
    # 오늘날짜의 식사만을 가져옴
    restaurant_list = Restaurant.objects.filter(school_id=school_id)
    #.filter(meal_date=datetime.now())
    meal_list = Meal.objects.filter(school_id=1).filter(meal_date=datetime.now())

    grouped_rest=dict()
    for obj in meal_list.all():
        name = restaurant_list.get(pk=obj.restaurant_id).name
        grouped_rest.setdefault((name,obj.time),[]).append(obj)

    grouped_time = dict()
    for key, value in grouped_rest.items():
        name = key[0]
        grouped_time.setdefault(name,[]).append((key[1],value))

    restaurant_dict = (grouped_time.items())

    context = {'restaurant_dict' : restaurant_dict}

    return render(request,'food/detail.html',context)


def restaurant_detail(request,school_id,restaurant_id):
    restaurant = Restaurant.objects.get(pk = restaurant_id)
    context = {'restaurant' : restaurant}

    return render(request,'food/detail_restaurant.html',context)


