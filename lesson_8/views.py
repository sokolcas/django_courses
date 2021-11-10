import csv
import datetime

from django.http import HttpResponse
# list_view используется, чтобы отобразить много элементов
from django.views.generic import ListView
from django.db.models import Q

from lesson_8.models import GameModel, GamerLibraryModel, GamerModel

# чтобы загрузить данные в бд с помощью csv файла
# ждя примера, чтобы работать дальше 
def upload_data(request):
    with open('vgsales.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            try:
                _, created = GameModel.objects.get_or_create(
                    name=row[1],
                    platform=row[2],
                    year=datetime.date(int(row[3]), 1, 1),
                    genre=row[4],
                    publisher=row[5],
                    na_sales=row[6],
                    eu_sales=row[7],
                    jp_sales=row[8],
                    other_sales=row[9],
                    global_sales=row[10],
                )
            except:
                pass
    return HttpResponse("Done!")


class FilterView(ListView):
    # когда мы передаем queryset, то в template нашем, который внизу
    # доступ к нему будет через {% for object in object_list%}
    # будем выводить данные в качестве таблицы
    template_name = 'gamemodel_list.html'
    # фильтруем все модели, название которых начинается с А, 
    # заканчивается а, содержат ma 
    queryset = GameModel.objects.filter(
        Q(name__startswith="A") & Q(name__endswith="a") & Q(
            name__contains="ma"))
    #  фильтр и по Q, и по имени
    queryset = GameModel.objects.filter(Q(name__endswith="a"),
                                        name__startswith="A")
    #  фильтр по или
    queryset = GameModel.objects.filter(
        Q(name__startswith="Ab") | Q(name__startswith="Ad") | Q(
            name__startswith="Mat"))
    #  фильтр с отрицанием. Не начинает с Ab и т.д.
    queryset = GameModel.objects.filter(
        ~Q(name__startswith="Ab") | ~Q(name__startswith="Ad") | ~Q(
            name__startswith="Mat"))


def relation_filter_view(request):
    # фильтрование по связанным полям. Фильтруем геймера по библиотеке
    data = GamerLibraryModel.objects.filter(gamer__email__contains="a")
    print(data[0].gamer.email)
    # return HttpResponse(data)
    # возвращаем отсортированные данные
    return HttpResponse(data.order_by())


class ExcludeView(ListView):
    template_name = 'gamemodel_list.html'
    # все записи, не имеющие слова Hitman
    queryset = GameModel.objects.exclude(name__contains="Hitman")


class OrderByView(ListView):
    template_name = 'gamemodel_list.html'
    # TODO add reverse
    # отсортировано по году в реверсивном порядке из-за -year
    queryset = GameModel.objects.exclude(name__contains="Hitman").order_by(
        '-year')
    # а можно так
    queryset = GameModel.objects.exclude(name__contains="Hitman").order_by(
        'year').reverse()


class AllView(ListView):
    template_name = 'gamemodel_list.html'
    # просто все записи
    queryset = GameModel.objects.all()


class UnionView(ListView):
    template_name = 'gamemodel_list.html'
    # два запроса. И тот, и тот. 
    queryset = GameModel.objects.filter(name="Hitman (2016)").union(
        GameModel.objects.filter(name="Tetris"))


class NoneView(ListView):
    template_name = 'gamemodel_list.html'
    # используется, когда нужен пустой queryset
    queryset = GameModel.objects.none()


class ValuesView(ListView):
    template_name = 'gamemodel_list.html'
    # вытянуть из модели конкретные поля объекта
    queryset = GameModel.objects.filter(name="Hitman (2016)").values("name",
                                                                     "platform",
                                                                     "year")

    def get(self, request, *args, **kwargs):
        # словарь
        print(GameModel.objects.filter(name="Hitman (2016)").values("name",
                                                                    "platform",
                                                                    "year"))
        # кортеж
        print(list(
            GameModel.objects.all().values_list("name", 'year')))
        # cписок значений, но только если одно поле указано
        print(list(
            GameModel.objects.all().values_list("name", flat= True)))
        return super().get(request, *args, **kwargs)


def date_view(request):
    # все объекты типа даты. kind - элемент, по которому обрезаем наши значения.
    # day = день, месяц, год; year- только год 
    data = GameModel.objects.dates(field_name='year', kind='year')
    print(data)
    return HttpResponse(data)


def get_view(request):
    # TODO try error
    # получили один объект
    data = GameModel.objects.get(id=27)
    print(data)
    return HttpResponse(data)


def create_view(request):
    # примитивный способ
    myself = GamerModel()
    myself.email = "admin@admin.com"
    myself.nickname = "SomeRandomNicknameSave"
    myself.save()
    # способ в одну строку
    myself = GamerModel(email="admin@admin.com",
                        nickname="SomeRandomNicknameSave")
    myself.save()
    # еще один способ, через кварги
    myself = GamerModel(**{"email": "admin@admin.com",
                           "nickname": "SomeRandomNicknameSave"})
    myself.save()
    # через create, save не пишем
    myself = GamerModel.objects.create(**{"email": "admin@admin.com",
                                          "nickname": "SomeRandomNicknameCreate"})
    # без кваргов
    myself = GamerModel.objects.create(email="admin@admin.com",
                                       nickname="SomeRandomNicknameCreate")
    # сразу много
    myself = GamerModel.objects.bulk_create([
        GamerModel(
            email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate1"),
        GamerModel(
            email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate2"),
        GamerModel(
            email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate3"),
        GamerModel(
            email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate4")
    ])
    # создали, указали на связь, потом сохранили
    my_library = GamerLibraryModel(gamer=GamerModel.objects.get(pk=10),
                                   size=10)
    my_library.save()
    # и только теперь делаем связь many to many, потому что нужен id элемента
    my_library.game.set([GameModel.objects.get(pk=1),
                         GameModel.objects.get(pk=2)])
    # через create
    my_library = GamerLibraryModel.objects.create(
        gamer=GamerModel.objects.get(pk=10),
        size=10)
    my_library.game.set([GameModel.objects.get(pk=1),
                         GameModel.objects.get(pk=2)])
    # много сразу. Хотя для связи многие ко многим не льзя, поэтому мы делаем 
    # bulc_create без отношений
    my_library = GamerLibraryModel.objects.bulk_create(
        [GamerLibraryModel(gamer=GamerModel.objects.get(pk=10),
                           size=10),
         GamerLibraryModel(gamer=GamerModel.objects.get(pk=10),
                           size=10)
         ])
    # проапдейтили нашу запись .
    my_friend = GamerModel.objects.get(pk=10)
    my_friend.update(nickname="MySecondNickname")
    return HttpResponse(my_friend)
