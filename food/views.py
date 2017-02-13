from django.shortcuts import render
from django.http import HttpResponse
from food.models import School, Restaurant, Meal #Post
from datetime import datetime
from django.template import loader, Context
from django.template.response import TemplateResponse
from food.forms import SoldOutForm # PostForm

# 매진되었을 때를 감안
check = False

def index(request):
    school_list = School.objects.all()
    context = {'school_list': school_list}

    return render(request, 'food/index.html', context)


def detail(request, shortname):
    # "레스토랑 이름 - 식사 시간 - 식사 이름" 으로 만들어줌.
    global check
    school = School.objects.get(shortname=shortname)
    restaurant_dict = School.detail_list(school.id, check)
    check = False
    context = {'school': school, 'restaurant_dict' : restaurant_dict, 'form' : SoldOutForm,}

    return render(request,'food/detail.html',context)


def restaurant_detail(request,shortname,restaurant_name):
    restaurant = Restaurant.objects.get(name=restaurant_name)
    #post = Post.objects.get(pk=pk)

    context = {'restaurant' : restaurant, #'post' : post
    }

    return render(request,'food/detail_restaurant.html',context)


def history(request,shortname):

    meal = request.GET['meal']
    meal_history = Meal.history(meal)
    template = loader.get_template('food/history.html')

    return TemplateResponse(request,template,{'meal_history':meal_history})

def bool(request,shortname):
    bool = request.POST['bool']
    meal_pk = request.POST['meal_pk']

    if bool == "false":
        Meal.objects.filter(id=meal_pk).update(soldout=True)
    else:
        Meal.objects.filter(id=meal_pk).update(soldout=False)

    global check
    check = True

    return HttpResponse("Success")

