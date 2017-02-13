from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from food.models import School, Restaurant, Meal, Comment
from datetime import datetime
from django.template import loader, Context
from django.template.response import TemplateResponse
from food.forms import SoldOutForm, CommentForm
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
    context = {'restaurant': restaurant,'shortname' : shortname, "restaurant_name": restaurant_name,'form' : CommentForm}
    if request.method == "POST":
        form = CommentForm(request.POST)
        #restaurant = Restaurant.objects.get(name=restaurant_name)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurant = restaurant
            comment.save()
            return render(request,'food/detail_restaurant.html',context)
    else :
        return render(request,'food/detail_restaurant.html',context)




def comment_edit(request, shortname,restaurant_name, pk):
    comment = Comment.objects.get(pk=pk)
    restaurant = Restaurant.objects.get(name=restaurant_name)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            context = {'restaurant': restaurant,'shortname' : shortname, "restaurant_name": restaurant_name,'form' : form,}
            return render(request,'food/detail_restaurant.html',context)
    else :
        form = CommentForm(instance=comment)
        context = {'restaurant': restaurant,'shortname' : shortname, "restaurant_name": restaurant_name,'form' : form,}
        return render(request,'food/detail_restaurant.html',context)


def comment_delete(request, shortname, restaurant_name, pk):
    comment = Comment.objects.get(pk=pk)
    restaurant = Restaurant.objects.get(name=restaurant_name)
    context = {'restaurant': restaurant,'shortname' : shortname, "restaurant_name": restaurant_name,'form' : CommentForm,}
    if request.method == 'POST':
        comment.delete()
        return render(request,'food/detail_restaurant.html',{'restaurant': restaurant,'shortname' : shortname, "restaurant_name": restaurant_name,'form' : CommentForm,})
    return render(request, 'food/comment_delete_confirm.html', {
        'comment': comment,
    })







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
    if request.body :
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
    else :
        return JsonResponse({
            'message' : {
            'text' : School.kakaotalk_list("서울대")
            }, :
            'keyboard' : {
            "type" : "buttons",
            "buttons" : ["서울대", "고려대", "한양대"]
            }
            })