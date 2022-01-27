from rest_framework import serializers
from django.contrib.auth import get_user_model

from hashes_apps.apps.hashes.models import Hash

UserModel = get_user_model()

class HashSerializer(serializers.ModelSerializer):
  def create(self, validated_data):
    return Hash(**validated_data)
  class Meta:
    model = Hash
    fields = ['id', 'hash', 'added_timestamp']