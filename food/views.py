from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from food.models import School, Restaurant, Meal #Post
from datetime import datetime
from django.template import loader, Context
from django.template.response import TemplateResponse
from food.forms import SoldOutForm # PostForm
import json

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
    #post = Post.objects.get(pk=pk)

    context = {'restaurant' : restaurant, #'post' : post
    }

    return render(request,'food/detail_restaurant.html',context)


def history(request,shortname):

    meal = request.GET['meal']
    meal_history = Meal.history(meal)
    template = loader.get_template('food/history.html')

    return TemplateResponse(request,template,{'meal_history':meal_history})


def keyboard(request):
    data = {
    "type" : "buttons",
    "buttons" : ["서울대", "고려대", "한양대"]
        }
    return JsonResponse(data)

@csrf_exempt
def message(request):
    json_str = (request.body).decode('utf-8')
    received_json_data = json.loads(json_str)
    name = received_json_data['content']

    return JsonResponse({
        'message' : {
        'text' : School.kakaotalk_list(name)
        },
        'keyboard' : {
        "type" : "buttons",
        "buttons" : ["서울대", "고려대", "한양대"]
        }
        })