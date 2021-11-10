from django.urls import path
from lesson_7 import views

urlpatterns = [
    path('try-form/', views.my_form, name='my_form'),
    path('class-form/', views.MyFormView.as_view(), name='class_form'),
    path('try-modelform/', views.ModelFormView.as_view(), name='modelform')
]
