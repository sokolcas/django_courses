from django.http import HttpResponse

from lesson_5.models import Flower, Bouquet, Client
from uuid import uuid4
from decimal import Decimal

from django.contrib.auth.models import User

from django.core.files import File


def create_flower(request):
    rose = Flower()
    rose.count = 10
    rose.description = "Роза является представителем семейства Разноцветных," \
                       " рода Шиповник. Растение в большинстве случаев " \
                       "представляет собой разветвленный кустарник, стебли" \
                       " которого покрыты шипами, роза имеет зеленые листья" \
                       " и большие ароматные цветы самого разного окраса"
    rose.wiki_page = "ссылка на википедию" # если не указать правильный url, будет использоваться дефолтное значение
    rose.could_use_in_bouquet = True
    rose.name = "Роза красная" # это поле уникальное, поэтому именя разные должны быть 
    rose.save() # сохранили наши значения, без них не добавится.  
    return HttpResponse("Created!")


def create_client(request):
    # другой способ создания объекта, используем kwargs, менеджер objects
    client = Client.objects.create(**{
        # чтобы создать клиента, надо добавить пользователя
        # связь один к одному обязательно для этого 
        # надо создать супер пользователя в Django 
        # python manage.py createsuperuser
        # username: admin, password: 1234, email - admin@amin.com
        #pk - primarykey
        'user': User.objects.get(pk=1),
        'second_email': 'admin@admin1.com',
        'name': 'MyName',
        # чтобы не хранить файлы в бд, храним их в локальной папке static/temp
        # в settings.py MEDIA_ROOT установим относительный путь 
        'invoice': File(open('requirements.txt')), 
        'user_uuid': uuid4(),
        'discount_size': Decimal("0.00052"),
        'client_ip': "192.0.2.1.",
    }) 
    return HttpResponse(client)


def get_flower(request):
    # получаем цену букета по id, для примера id=1
    price = Bouquet.shop.get(id=1).price
    return HttpResponse(price)
