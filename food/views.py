from django.shortcuts import render
from django.http import HttpResponse
from food.models import School, Restaurant, Meal
# Create your views here.
def index(request):
    school_list = School.objects.all()
    context = {'school_list': school_list}

    return render(request, 'food/index.html',context)


def detail(request,school_id):
    restaurant_list = Restaurant.objects.filter(school_id=school_id)
    context = {'school_id':school_id,'restaurant_list': restaurant_list}

    return render(request,'food/detail.html',context)


def restaurant_detail(request,school_id,restaurant_id):
    restaurant = Restaurant.objects.get(pk = restaurant_id)
    context = {'restaurant' : restaurant}
    return render(request,'food/detail_restaurant.html',context)


