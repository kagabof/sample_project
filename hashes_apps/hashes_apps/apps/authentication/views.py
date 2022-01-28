import json
from django.db import IntegrityError
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from hashes_apps.apps.authentication.serializers import CreateUserSerializer
from hashes_apps.apps.authentication.models import User
from hashes_apps.utils.create_user_token import create_user_token


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def create_user(request):
    try:
        data = {}
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user: User = serializer.save()
            user.is_active = True
            user.save()
            data["message"] = "User have registered successfully"
            data["email"] = user.email
            data["username"] = user.username
        else:
            data = serializer.errors
        return Response(data, HTTP_201_CREATED)
    except IntegrityError as e:
        return Response({"Error": f'{str(e)}'}, HTTP_400_BAD_REQUEST)

    except KeyError as e:
        return Response({"Error": f'Field {str(e)} missing'},
                        HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def user_login(request):
    data = {}
    req_data = json.loads(request.body)
    try:
        user = User.objects.get(email=req_data.get("email"))
    except Exception as e:
        return Response({"Error": f'{str(e)}'}, HTTP_400_BAD_REQUEST)
    user_auth = authenticate(
        username=req_data.get("email"),
        password=req_data.get("password"))
    if not user_auth:
        data["error"] = "Invalid credentials"
        return Response(data=data, status=HTTP_400_BAD_REQUEST)

    else:
        data["message"] = "User logged in successfully"
        data.update(create_user_token(user))
        return Response(data, HTTP_201_CREATED)
