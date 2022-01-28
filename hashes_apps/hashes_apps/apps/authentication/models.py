from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models import F


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        check_email = self.model.objects.filter(email=email).first()
        if not email and check_email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(username),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = user.is_staff = True
        user.is_active = user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, null=True)
    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = [F('username').asc(nulls_last=True)]

    def __str__(self):
        return str(self.email)
