from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, nickname, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            nickname=nickname,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            nickname=nickname,
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        db_table = 'user'


class Vegan(models.Model):
    VEGAN_LEVEL_CHOICE = [
        ('Vegan', 'Vegan'),
        ('Lacto', 'Lacto'),
        ('Ovo', 'Ovo'),
        ('Lacto Ovo', 'Lacto Ovo'),
        ('Pesco', 'Pesco'),
        ('Pollo', 'Pollo'),
        ('Flexitarian', 'Flexitarian'),
        ('NonVegan', 'NonVegan'),
    ]
    level = models.CharField(max_length=11, choices=VEGAN_LEVEL_CHOICE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vegan'


class CO2Cal(models.Model):
    level = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'co2'


class Challenge(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.CharField(max_length=10, null=False, blank=False)
    people_num = models.IntegerField(default=0, null=False, blank=False)
    content = models.TextField(blank=False)
    check_method = models.CharField(max_length=50, null=False, blank=False)
    money = models.IntegerField(default=0, null=False, blank=False)
    chat_link = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    finished = models.BooleanField(default=False)

    class Meta:
        db_table = 'challenge'


class GroupPurchase(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    people_num = models.IntegerField(default=0)
    product_link = models.CharField(max_length=100, null=False, blank=False)
    chat_link = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    finished = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = 'group_purchase'
