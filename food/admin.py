from django.contrib import admin
from food.models import School,Restaurant,Meal,Comment

## admin 페이지에 크롤링 버튼을 만들고자 함
## 방법을 아직 모르겠음.

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_url']
    list_display_links = ['id','name']
    search_fields = ['name']
    actions = ['crawl']

    def crawl(self, request, queryset):
        Meal.crawl_SCHOOL(queryset)
        self.message_user(request, '수행!!')
        pass
    crawl.short_description = '지정 학교를 크롤링합니다.'


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id','name','location','school']
    list_display_links = ['id','name']
    list_filter = ['school']
    search_fields = ['name']


class MealAdmin(admin.ModelAdmin):
    list_display = ['id','name','time','meal_date','restaurant','school']
    list_display_links = ['id','name']
    list_filter = ['school', 'restaurant']
    search_fields = ['name']

    def delete_model(self,request,obj):
        for o in obj.all():
            o.delete()
    delete_model.short_description = 'Delete flow'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant','message']
    list_display_links = ['id','message']
    list_filter = ['restaurant']
    search_fields = ['message']

admin.site.register(School, SchoolAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Comment, CommentAdmin)

