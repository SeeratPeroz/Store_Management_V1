from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, username, userPhone, password=None):
        if not username:
            raise ValueError("Their should be username.")

        user = self.model(
            username=username,
            userPhone=userPhone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, username, userPhone, userAdd, password=None, is_admin = False):
        user = self.model(
            username=username,
            userAdd=userAdd,
            userPhone=userPhone,
        )
        user.set_password(password)
        user.save(using=self._db)

        user.is_admin = False
        user.is_active = True
        user.is_staff = True
        return user

    def create_superuser(self, username, userPhone, password):
        user = self.create_user(
            username=username,
            userPhone=userPhone,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=60, unique=True)
    userPhone = models.CharField(max_length=15)
    userAdd = models.CharField(max_length=100)
    date_joined = models.DateTimeField(verbose_name='Date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['userPhone']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
