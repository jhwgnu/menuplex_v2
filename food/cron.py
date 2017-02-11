from food.models import School, Restaurant, Meal

## 시간에 따라 자동으로 크롤링 하도록 설정해주는 .py 파일
## 윈도우 환경에서 돌아가지 않음.

def scheduled_job():
    Meal.crawl_SNU()
    Meal.crawl_KU()
    Meal.crawl_HYU()
