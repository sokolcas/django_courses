"""django_courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lesson_1/', include('lesson_1.urls')),
    path('lesson_2/', include('lesson_2.urls')),
    path('lesson_3/', include('lesson_3.urls')),
    path('lesson_5/', include('lesson_5.urls')),
    path('lesson_7/', include('lesson_7.urls')),
    path('lesson_8/', include('lesson_8.urls')),
    path('lesson_9/', include('lesson_9.urls')),
    
]
