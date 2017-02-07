from django.contrib import admin
from food.models import School,Restaurant,Meal

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_url']
    list_display_links = ['id','name']
    search_fields = ['name']


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id','name','location','school']
    list_display_links = ['id','name']
    search_fields = ['name']


class MealAdmin(admin.ModelAdmin):
    list_display = ['id','name','time','meal_date','price','restaurant','school']
    list_display_links = ['id','name']
    search_fields = ['name']


admin.site.register(School, SchoolAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Meal, MealAdmin)
