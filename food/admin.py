from django.contrib import admin
from food.models import School,Restaurant,Meal

## admin 페이지에 크롤링 버튼을 만들고자 함
## 방법을 아직 모르겠음.

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_url']
    list_display_links = ['id','name']
    search_fields = ['name']


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id','name','location','school']
    list_display_links = ['id','name']
    search_fields = ['name']


class MealAdmin(admin.ModelAdmin):
    list_display = ['id','name','time','meal_date','restaurant','school']
    list_display_links = ['id','name']
    search_fields = ['name']

    def delete_model(self,request,obj):
        for o in obj.all():
            o.delete()
    delete_model.short_description = 'Delete flow'

admin.site.register(School, SchoolAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Meal, MealAdmin)
