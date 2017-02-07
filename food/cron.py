from food.models import School, Restaurant, Meal
def scheduled_job():
    Meal.crawl_SNU()
