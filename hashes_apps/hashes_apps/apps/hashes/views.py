import json
from django.conf import settings
from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from hashes_apps.apps.authentication.models import User
from hashes_apps.apps.hashes.serializers import HashSerializer
from hashes_apps.apps.hashes.models import Hash

UserModel = get_user_model()

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_hash(request):
  try:
    user_email = request.user
    req_data = json.loads(request.body)
    data = {}
    user:User =  UserModel.objects.filter(email=user_email).first()
    hash_instance = Hash(
      hash=req_data["hash"],
      user=user
    )
    serializer = HashSerializer(instance=hash_instance, data=request.data)
    if serializer.is_valid():
      if len(req_data["hash"]) == int(settings.HASH_LENGTH[0]):
        hash:Hash = serializer.save()
        data["massage"] = "Hash Created successfully"
        data["id"] = hash.id
        data["hash"] = hash.hash
        data["timestamp"] = hash.added_timestamp
      
        return Response(data)
      else:
        return Response({
            "Error": f"Your hash length must be {settings.HASH_LENGTH}"
          },status=HTTP_400_BAD_REQUEST)

    return Response({"Error": "Bad request!"}, status=HTTP_400_BAD_REQUEST)
  except IntegrityError as e:
    raise ValidationError({"400": f'{str(e)}'})
  except KeyError as e:
    raise ValidationError({"400": f'Field {str(e)} missing'})
