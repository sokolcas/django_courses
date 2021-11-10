from django.urls import path
from lesson_2 import views


urlpatterns = [

    path('', views.index, name='index'),
    path('article/<int:year>/', views.year_archive),
    
    path('index/', views.index, name= 'index-view'), # www.yandex.ru/index/
    path('bio/<username>/', views.bio, name = 'bio'), # www.yandex.ru/bio/admin/
]