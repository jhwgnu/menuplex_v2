from django.shortcuts import render
from django.http import HttpResponse
from food.models import School, Restaurant, Meal
from datetime import datetime
# Create your views here.
def index(request):
    school_list = School.objects.all()
    context = {'school_list': school_list}

    return render(request, 'food/index.html', context)

def detail(request,shortname):
    # "레스토랑 이름 - 식사 시간 - 식사 이름" 으로 만들어줌.
    school = School.objects.get(shortname=shortname)
    restaurant_dict = School.detail_list(school.id)
    context = {'school': school, 'restaurant_dict' : restaurant_dict}

    return render(request,'food/detail.html',context)


def restaurant_detail(request,shortname,restaurant_name):
    restaurant = Restaurant.objects.get(name=restaurant_name)
    context = {'restaurant' : restaurant}

    return render(request,'food/detail_restaurant.html',context)
