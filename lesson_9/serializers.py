from rest_framework import serializers
from lesson_8.models import GamerLibraryModel, GamerModel, GameModel
from django.contrib.auth.models import User

class GameModelSerializer(serializers.ModelSerializer):
    class Meta:
        # указываем модель
        model = GameModel
        # указываем поля
        fields = '__all__'


class GamerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamerModel
        fields = ['nickname', 'email']

# сериалайзер для пользователя, для создания
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        # пароль только записать можем. Читать пароли нельзя
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
