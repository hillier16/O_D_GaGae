from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable

GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )


class UserManager(BaseUserManager):
    def create_user(self, uid, name, password=None, **extra_fields):
        user = self.model(
            uid=uid,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, name, password, **extra_fields):
        user = self.create_user(
            uid,
            name,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    uid = models.CharField(primary_key=True, unique=True, max_length=100)
    name = models.CharField(max_length=20, null=False,)
    gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    age = models.IntegerField(default=0, blank=True)
    survey_coin = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)   # True: 로그인, False: 로그아웃
    is_admin = models.BooleanField(default=False)   # True: 관리자, False: 사용자
    joined_date = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'uid'    # 유니크 식별자로 사용
    REQUIRED_FIELDS = ['name']  # createsuperuser 커맨드로 유저를 생성할 때 나타날 필드 이름 목록

    def __str__(self):
        return str(self.pk)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class PersonalSchedule(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)


class TimeTable(models.Model):
    DAY_CHOICES = (
        ('1', '월요일'),
        ('2', '화요일'),
        ('3', '수요일'),
        ('4', '목요일'),
        ('5', '금요일'),
        ('6', '토요일'),
        ('7', '일요일'),
    )
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=20)
    day = models.CharField(max_length=1, default='0', choices=DAY_CHOICES)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)


class Alarm(models.Model):
    target = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    generated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    generated_date = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=10) # random하게 생성되어야 함(알파벳, 숫자 조합)
    member_num = models.IntegerField(default=1)

    def __str__(self):
        return str(self.pk)


class GroupMember(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    member = models.ForeignKey('User', on_delete=models.CASCADE)
    joined_date = models.DateTimeField(default=timezone.now)
    is_alarm_on = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)


class GroupSchedule(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)


class GroupNotice(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    generated_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class GroupBoard(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    generated_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='User_for_author')
    person_in_charge = models.ManyToManyField('User', blank=True, related_name='User_for_person_in_charge')

    def __str__(self):
        return str(self.pk)


class Survey(models.Model):
    AGE_CHOICES = (
        (1, '10대'),
        (2, '20대'),
        (3, '30대'),
        (4, '40대'),
        (5, '50대')
    )
    title = models.TextField()
    description = models.TextField()
    target_age_start = models.IntegerField(default=1, choices=AGE_CHOICES)
    target_age_end = models.IntegerField(default=5, choices=AGE_CHOICES)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    target_gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    used_coin = models.IntegerField(default=0)
    edited_date = models.DateTimeField(default=timezone.now)
    generated_date = models.DateTimeField(default=timezone.now)
    answer_num = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)


class SurveyQuestion(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    index = models.IntegerField()
    content = models.TextField()
    question_type = models.IntegerField(default=0) # 0: 객관식, 1: 주관식
    choices = models.TextField() # 객관식 보기 리스트: 구분자(;)로 구분

    def __str__(self):
        return str(self.pk)


class SurveyAnswer(models.Model):
    survey_question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return str(self.pk)