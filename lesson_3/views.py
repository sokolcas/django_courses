from django.http import HttpResponse, FileResponse, HttpResponseRedirect, \
    HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
import re
import os
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.template import loader, RequestContext

#добавил функцию, которая нормализирует путь через регулярки
def path_normalize(path: str):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_abs = BASE_DIR+static(path)
    path = re.sub(r'[\/\\]', r'\\', path_abs)

    return path 

class MyView(View):
    def get(self, request):
        print(request.GET)
        if request.GET.get('type') == "file":
            img_path = path_normalize('img/img1.jpg')
            return FileResponse(open(img_path, "rb+")) 
        elif request.GET.get('type') == "json":
            return JsonResponse({i: i + i for i in range(1, 20)}, safe=False)
        elif request.GET.get('type') == "redirect":
            return HttpResponseRedirect("http://127.0.0.1:8000/admin")
        else:
            return HttpResponseNotAllowed("You shall not pass!!!")
    def post(self, request):
        print(request.POST)
        return HttpResponse("This is POST")

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def main(request):
    # в контенте в переменные 'str' и 'int' передали значения, которые можем вызывать в шаблоне(html файле), используя {{str}}
    test_template = loader.render_to_string("main.html", context={'str': 'Test string', 'int':12}, request=None, using=None)
    test_template = loader.select_template("main.html")

    return HttpResponse(test_template)



def text(request):
    return HttpResponse("This is text from backend to user interface")


def file(request):
    print(static('img/img1.jpg'))
    #отвечаем файлом
    # ну поехали нахуй 
    # здесь изначально было open(static('img/img1.jpg', "rb+"))
    # Но это нихера не работает, потому что путь берется как path + STATIC_URL = 'lesson_3/static/' + img/img1.jpg
    # Так можно делать на маке или удаленном сервере, у нас виндовс и поэтому путь у нас прописывается по другому. 
    #return FileResponse(open('C:\\Users\\cas\\Desktop\\Data Science\\python\\django\\django_courses\\lesson_3\\static\\img\\img1.jpg', "rb+")) 
    img_path = path_normalize('img/img1.jpg')
    return FileResponse(open(img_path, "rb+")) 

def redirect(request):
    #перенаправляем пользователя
    return HttpResponseRedirect("http://www.google.com")


def not_allowed(request):
    # нет доступа
    return HttpResponseNotAllowed("You shall not pass!!!")


def json(request):
    # возвращаем json 
    return JsonResponse({i: i + i for i in range(1, 20)}, safe=False)