from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, nickname, email, password, **kwargs):
        user = self.model(
            nickname=nickname,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(models.Model):
    nickname = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'


class Vegan(models.Model):
    level = models.CharField(max_length=5, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vegan'


class CO2Cal(models.Model):
    level = models.CharField(max_length=5, null=False, blank=False)
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
