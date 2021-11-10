from django.urls import include, path
from rest_framework import routers
from lesson_9 import views

from django.contrib import admin

router = routers.SimpleRouter()
# router генерирует запросы
# автоматом url генеряться
router.register(r'view-set', views.ViewSetAPIView)
router.register(r'game', views.GameViewSet)
router.register(r'gamer', views.GamerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path('function/', views.view_function, name='function_view'),
    path('class/', views.ClassAPIView.as_view(), name='class_view'),
    path('generic/', views.MyCreateAPIView.as_view(), name='generic'),
    path('retrieve/<int:pk>', views.MyRetrieveAPIView.as_view(),
         name='retrieve'),
    path('retrieve-update/<int:pk>', views.MyRetrieveUpdateAPIView.as_view(),
         name='retrieve_update'),
    path('api-login', views.user_login),
    path('create-user', views.CreateUser.as_view())
]
