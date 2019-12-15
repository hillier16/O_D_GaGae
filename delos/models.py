from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        user = self.create_user(
            email,
            name,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=20,
        null=False,
    )
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    sex = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    age = models.IntegerField()
    department = models.CharField(max_length=20)
    survey_coin = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'    # 유니크 식별자로 사용
    REQUIRED_FIELDS = ['name', 'age', 'department']  # createsuperuser 커맨드로 유저를 생성할 때 나타날 필드 이름 목록

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Member(models.Model):
    group_pk = models.ForeignKey('Group', on_delete=models.CASCADE)
    member = models.ForeignKey('User', on_delete=models.CASCADE)
    authority = models.BooleanField()

    def __str__(self):
        return self.member


class Groupschedule(models.Model):
    group_pk = models.ForeignKey('Group', on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.group_pk


class Timeschedule(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title


class Group(models.Model):
    group_name = models.CharField(max_length=255)
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class Survey(models.Model):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    link = models.TextField()
    target_gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    # target_age 나이대 저장 방법 이슈
    used_coin = models.IntegerField(default=0)
    deadline = models.DateTimeField()
    generated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author
