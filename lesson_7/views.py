import os

from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.shortcuts import render

from lesson_7.forms import MyForm, FormFromModel


def my_form(request):
    print(request.FILES)
    # запрос передается в форму, в данном случае пост 
    form = MyForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        print(form.cleaned_data)
        # соединяем наш путь + медиа рут + название файла из реквеста
        file_path = os.path.join(settings.MEDIA_ROOT,
                                 form.cleaned_data['profile_picture'].name)
        # дальше дописываем название картинки в локальный файл
        # цикл используется, чтобы большие файлы записывать кусками. 
        with open(file_path, 'wb+') as local_file:
            for chunk in form.cleaned_data['profile_picture']:
                local_file.write(chunk)
    else:
        print(form.errors)

    return render(request, 'form_page.html', context={'form': form})

# опишем класс, который делает тоже самое, что и функция выше
# валидация прописана сама в FormView
class MyFormView(FormView):
    # класс формы, которая будет отрабатывать
    form_class = MyForm
    template_name = "form_page.html"
    # описываем метод GET
    def get(self, request, *args, **kwargs):
        print(request.GET)
        return super().get(request,  *args, **kwargs)

# так используют формы в реальных проектах
# используем форму по модели
class ModelFormView(FormView):
    form_class = FormFromModel
    template_name = "model_from_page.html"
    # чтобы перенаправить пользователя на страницу, которая нужна,
    # после того, как пользователь нажал субмит
    success_url = reverse_lazy("modelform")

    def form_valid(self, form):
        # нужно помнить, что форму нужно сохранять, чтобы форма сохранила данные в модель
        # а модель в бд
        form.save()
        return super().form_valid(form)
