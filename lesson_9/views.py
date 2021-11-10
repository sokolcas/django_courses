from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView

from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from lesson_8.models import GameModel, GamerModel
from lesson_9.serializers import GameModelSerializer, GamerModelSerializer, UserSerializer


from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK

class GameViewSet(viewsets.ModelViewSet):
    queryset = GameModel.objects.all().order_by('-year')
    serializer_class = GameModelSerializer


class GamerViewSet(viewsets.ModelViewSet):
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer

@csrf_exempt
# чтобы использовать функцию как view для метода, указанного в скобках
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(request):
    # получаем от пользователя его логин и пароль
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please username and password'})
    # пытаемся пройти аутентификацию пользователя
    user = authenticate(username=username, password=password)
    # прошла ли аутентификация?
    if not user:
        return Response({'error': 'Invalid data'})
    # создаем токен для пользователя
    # токен в таблицу в бд отправляется
    token, _ = Token.objects.get_or_create(user=user)
    # другой response
    # отпраялем токен пользователю
    return Response({'token': token.key}, status=HTTP_200_OK)

# чтобы создать учетную запись для пользователя
class CreateUser(CreateAPIView):
    # указываем разрешения для пользователя
    permission_classes = (AllowAny,)
    # сериалайзер для учетных записей
    serializer_class = UserSerializer

# чтобы проверять csrf токен
@csrf_exempt
# чтобы использовать функцию как view для метода, указанного в скобках
@api_view(['GET', 'POST'])
# @api_view()
def view_function(request):
    print(request.data)
    return Response({'test': 'some_function_data'})

# наследуемся и определяем действия
# этот класс можно настроить под нашу необходимость
class ClassAPIView(APIView):

    def get(self, request):
        return Response({'class': 'some_class_data'})

    def post(self, request):
        print(request.data)
        return Response({'class': 'some_class_data'})

# вместо отдельной функции на каждое действие
class ViewSetAPIView(viewsets.ViewSet):
    # общий queryset для всех
    queryset = GameModel.objects.filter(id__lte=10)
    # выведем список элементов
    def list(self, request):
        # чтобы обработать данные и отправить JSON
        serializer = GameModelSerializer(self.queryset, many=True)
        return Response(serializer.data)
    #  получить один элемент, для этого в адрессной строке /номер элемента
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = GameModelSerializer(user)
        return Response(serializer.data)

# еще проще, чем выше. Он сам создает уже большинство функций
# нужно только указать сериализатор, чтобы указать данные.
class MyCreateAPIView(CreateAPIView):
    serializer_class = GamerModelSerializer

# чтобы получить данные
class MyRetrieveAPIView(RetrieveAPIView):
    # прописываем разрешения, только админам разрешаем
    permission_classes = (IsAdminUser,)
    # здесь нужно указать queryset, какие данные получать, с фильтром
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer

# чтение и дополнение
class MyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer
