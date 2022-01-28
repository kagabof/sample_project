from rest_framework import pagination
import json
from django.conf import settings
from django.db import IntegrityError
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from hashes_apps.apps.authentication.models import User
from hashes_apps.apps.hashes.serializers import HashSerializer
from hashes_apps.apps.hashes.models import Hash
from scipy import spatial

UserModel = get_user_model()


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100


paginator = CustomPagination()


@api_view(["POST", "GET"])
@permission_classes([permissions.IsAuthenticated])
def create_hash(request):
    if request.method == "POST":
        try:
            user_email = request.user
            req_data = json.loads(request.body)
            data = {}
            user: User = UserModel.objects.filter(email=user_email).first()
            hash_instance = Hash(
                hash=req_data["hash"],
                user=user
            )
            serializer = HashSerializer(
                instance=hash_instance, data=request.data)
            if serializer.is_valid():
                if len(req_data["hash"]) == int(settings.HASH_LENGTH[0]):
                    hash: Hash = serializer.save()
                    data["message"] = "Hash Created successfully"
                    data["id"] = hash.id
                    data["hash"] = hash.hash
                    data["timestamp"] = hash.added_timestamp

                    return Response(data)
                else:
                    return Response({
                        "Error":
                        f"Your hash length must be {settings.HASH_LENGTH}"
                    }, status=HTTP_400_BAD_REQUEST)

            return Response({"Error": "Bad request!"},
                            status=HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"Error": f'{str(e)}'},
                            HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({"Error": f'Field {str(e)} missing'},
                            HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        queryset = Hash.objects.all()
        hash_page_result = paginator.paginate_queryset(queryset, request)
        serializer = HashSerializer(hash_page_result, many=True)
        data = {}
        data["hashes"] = serializer.data
        data["message"] = "Hashes found successfully" if len(
            serializer.data) else "Oops! no hash found!"
        data["count"] = len(serializer.data)
        return Response(data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_hash(request, pk):
    queryset = Hash.objects.filter(id=pk).first()
    if not queryset:
        return Response(
            {"Error": f'Hash with {str(pk)} does not exist'},
            HTTP_400_BAD_REQUEST)
    serializer = HashSerializer(queryset, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_hash_by_the_nearest(request, pk):
    base_hash: Hash = Hash.objects.filter(id=pk).first()
    if not base_hash:
        return Response(
            {"Error": f'Hash with {str(pk)} does not exist'},
            HTTP_400_BAD_REQUEST)
    else:
        all_hash = Hash.objects.exclude(id=pk).all()
        all_hashes_with_distance = []
        for le in all_hash:
            hash: Hash = le
            new_hash = {}

            # Find the distance
            distance, _ = spatial.KDTree([hash.hash]).query(base_hash.hash)
            new_hash["distance"] = distance
            new_hash["data"] = HashSerializer(hash, many=False).data
            all_hashes_with_distance.append(new_hash)

        sorted_list = sorted(all_hashes_with_distance,
                             key=lambda i: i['distance'])
        selected_data_hash = HashSerializer(base_hash, many=False).data

        return Response({
            "hash_selected": selected_data_hash,
            "near_hashes": sorted_list,
            "message": "Hashes found successfully"
        })
