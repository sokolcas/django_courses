from django.db import models
from datetime import timedelta

# в джанго есть встроенная модель пользователя и можно использовать ее, а не писать свою
from django.contrib.auth.models import User

#создадим 3 модели для цветочного магазина

#модель цветов
class Flower(models.Model):
    #сколько цветков, по дефолту = 0, поле может быть пустым.
    count = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField(null=True)
    #auto_now_add - фиксирует время сейчас автоматически. По дефолту. 
    delivered_at = models.DateTimeField(auto_now_add=True, blank=True,
                                        null=True)
    could_use_in_bouquet = models.BooleanField(default=True, null=True)
    # unique_for_date - дата уникальная 
    wiki_page = models.URLField(default="https://www.wikipedia.org/",
                                name="wikipedia",
                                unique_for_date="delivered_at", null=True)
    #max_length - обязательный атрибут
    name = models.CharField(max_length=64, unique=True, null=True)

#модель букетов
class Bouquet(models.Model):
    #переименуем наш менеджер
    shop = models.Manager()
    # сколько времени букем может быть свежим. 
    # timedelta - от нынешнего дня отсчитываем 5 дней. 
    fresh_period = models.DurationField(default=timedelta(days=5), null=True,
                                        help_text="Use this field when you need"
                                                  " to have information about "
                                                  "bouquet fresh time")
    photo = models.ImageField(blank=True, null=True)
    price = models.FloatField(default=1.0, null=True)
    # разные цветы могут быть в разных букетах, указываем, какой класс связан с этим. 
    flowers = models.ManyToManyField(Flower,
                                     verbose_name="This bouquet"
                                                  " consists of this flowers")

#модель клиентов
class Client(models.Model):
    # соединяем нашего клиента со стандартным пользователем Django, чтобы не писать лишнего.
    # такой прием называется UserProfile, когда у нас создается наш User,
    # у нас сразу будет возможность добавить к нему поля, описанные ниже
    #  если мы удалим нащего пользователя, то будем удалять все связанное с ним каскадно. 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    second_email = models.EmailField(null=True)
    name = models.CharField(max_length=64, null=True)
    # накладная. Прикрепляем накладную
    # upload_to - куда мы сохраняем файл
    # uploads/%Y/%m/%d/ - паттерн, автоматом создает папки c нынешней датой
    invoice = models.FileField(null=True, upload_to='uploads/%Y/%m/%d/')
    user_uuid = models.UUIDField(editable=False, null=True)
    # размер скидки, max_digits - максимальная цифра, максимум скидки
    #decimal_places - сколько знаков после запятой
    discount_size = models.DecimalField(max_digits=5, decimal_places=5,
                                        null=True) 
    client_ip = models.GenericIPAddressField(blank=True, null=True,
                                             protocol="IPv4")

# функция дескриптер, которая определяет как будет выглядеть объект 
# нашей модели при выводе его на экран 
    def __str__(self):
        return self.name
