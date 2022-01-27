from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email')


class CreateUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  def create(self, validated_data):
    user = UserModel.objects.create_user(
      username=validated_data['username'],
      password=validated_data['password'],
      email=validated_data['email'],
    )
    return user

  class Meta:
    model = UserModel
    fields = ( "id", "username", "password", "email")
