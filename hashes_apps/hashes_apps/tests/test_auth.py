from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from hashes_apps.apps.authentication.models import User

client = APIClient()
UserModel = get_user_model()


class UserSignUpTestCase(TestCase):
    def setUp(self):
        data = {
            "email": "fofo12345fef@gmail.com",
            "password": "dede",
            "username": 'kagabo'
        }
        user: User = UserModel.objects.create_user(
            **data
        )
        user.save()
        response = client.post('/auth/login', {
            "email": "fofo12345fef@gmail.com",
            "password": "dede",
        }, format='json')
        assert "refresh" in response.data
        assert "access" in response.data
        assert "message" in response.data
        self.user_instance: User = user
        self.user_token = response.data["access"]

    def test_create_user(self):
        """Test create user
        """
        data = {
            "username": "kagabo",
            "email": "fofo1234@gmail.com",
            "password": "dede"
        }
        response = client.post('/auth/create', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "User have registered successfully"
        assert response.data["email"] == data["email"]
        assert response.data["username"] == "kagabo"

    def test_login_user(self):
        """Test login
        """

        data = {
            "email": "fofo12345@gmail.com",
            "password": "dede",
            "username": 'kagabo'
        }
        user: User = UserModel.objects.create_user(
            **data
        )
        user.save()
        response = client.post('/auth/login', {
            "email": "fofo12345@gmail.com",
            "password": "dede",
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert "refresh" in response.data
        assert "access" in response.data
        assert "message" in response.data
        assert response.data["message"] == "User logged in successfully"

    def test_create_hash(self):
        """Test create hash
        """
        hash = [3, 6]
        response = client.post('/hash/', {
            "hash": hash
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')

        assert response.status_code == status.HTTP_200_OK
        assert "id" in response.data
        self.hash_1 = response.data["id"]
        assert "message" in response.data
        assert "hash" in response.data
        assert "hash" in response.data
        assert response.data["hash"] == hash

    def test_get_hash_by_id(self):
        """Test get one hash by id
        """
        hash = [6, 8]
        response_new = client.post('/hash/', {
            "hash": hash
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        assert response_new.status_code == status.HTTP_200_OK
        assert "id" in response_new.data

        response = client.get(
            f'/hash/{response_new.data["id"]}',
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')

        assert response.status_code == status.HTTP_200_OK
        assert "id" in response.data
        assert "hash" in response.data
        assert "hash" in response.data
        assert response.data["hash"] == hash

    def test_all_hash(self):
        """Test all hashes
        """
        hash_1 = [6, 8]
        hash_2 = [4, 5]
        hash_3 = [2, 7]
        hash_4 = [3, 6]
        client.post('/hash/', {
            "hash": hash_1
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        client.post('/hash/', {
            "hash": hash_2
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        client.post('/hash/', {
            "hash": hash_3
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        response_new = client.post('/hash/', {
            "hash": hash_4
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        assert response_new.status_code == status.HTTP_200_OK
        assert "id" in response_new.data

        response = client.get(
            '/hash/',
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["hashes"]) == 4
        assert "message" in response.data
        assert "count" in response.data
        assert response.data["count"] == 4
        assert response.data["message"] == "Hashes found successfully"

    def test_get_hash_by_the_nearest(self):
        """Test all hashes
        """
        hash_1 = [6, 8]
        hash_2 = [4, 5]
        hash_3 = [2, 7]
        hash_4 = [3, 6]
        client.post('/hash/', {
            "hash": hash_1
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        client.post('/hash/', {
            "hash": hash_2
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        client.post('/hash/', {
            "hash": hash_3
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        response_new = client.post('/hash/', {
            "hash": hash_4
        }, HTTP_AUTHORIZATION=f"Bearer {self.user_token}", format='json')
        assert response_new.status_code == status.HTTP_200_OK
        assert "id" in response_new.data

        response = client.get(
            f'/hash/sort_by_nearest/{response_new.data["id"]}',
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
            format='json')

        assert response.status_code == status.HTTP_200_OK
        assert "hash_selected" in response.data
        assert "near_hashes" in response.data
        assert len(response.data["near_hashes"]) == 3
        assert response.data["near_hashes"][0]["data"]["hash"] == hash_3
        assert response.data["message"] == "Hashes found successfully"
