from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.utils import timezone

GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )

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
    gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    date_of_birth = models.DateTimeField()
    department = models.CharField(max_length=20)
    survey_coin = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True) # True: 로그인, False: 로그아웃
    is_admin = models.BooleanField(default=False) # True: 관리자, False: 사용자
    joined_date = models.DateTimeField(auto_now_add=True)
    signup_method = models.IntegerField(default=0) # 0: 자체 회원가입, 1: 카카오톡

    objects = UserManager()

    USERNAME_FIELD = 'email'    # 유니크 식별자로 사용
    REQUIRED_FIELDS = ['name', 'date_of_birth', 'department']  # createsuperuser 커맨드로 유저를 생성할 때 나타날 필드 이름 목록

    def __str__(self):
        return self.email

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
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner)


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
        return self.title


class Alarm(models.Model):
    target = models.ForeignKey('User', on_delete=models.CASCADE)
    group_pk = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.group_pk)


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10) # random하게 생성되어야 함(알파벳, 숫자 조합)
    member_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group_pk = models.ForeignKey('Group', on_delete=models.CASCADE)
    member = models.ForeignKey('User', on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_alarm_on = models.BooleanField(default=True)

    def __str__(self):
        return str(self.member)


class GroupSchedule(models.Model):
    group_pk = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.group_pk)


class GroupNotice(models.Model):
    group_pk = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author)


class GroupBoard(models.Model):
    group_pk = models.ForeignKey('Group', on_delete=models.CASCADE)
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='User_for_author')
    person_in_charge = models.ManyToManyField('User', blank=True, related_name='User_for_person_in_charge')

    def __str__(self):
        return str(self.author)


class Survey(models.Model):
    AGE_CHOICES = (
        ('1', '10대'),
        ('2', '20대'),
        ('3', '30대'),
        ('4', '40대'),
        ('5', '50대')
    )
    target_age_start = models.CharField(max_length=1, default='1', choices=AGE_CHOICES)
    target_age_end = models.CharField(max_length=1, default='5', choices=AGE_CHOICES)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    target_gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    used_coin = models.IntegerField(default=0)
    edited_date = models.DateTimeField()
    generated_date = models.DateTimeField(auto_now_add=True)
    answer_num = models.IntegerField(default=0)
    is_active = models.BooleanField(defualt=True)

    def __str__(self):
        return str(self.author)


class SurveyQuestion(models.Model):
    survey_pk = models.ForeignKey('Survey', on_delete=models.CASCADE)
    index = models.IntegerField()
    content = models.TextField()
    question_type = models.IntegerField(default=0) # 0: 객관식, 1: 주관식
    choices = models.TextField() # 객관식 보기 리스트: 구분자(;)로 구분

    def __str__(self):
        return self.content


class SurveyAnswer(models.Model):
    survey_question_pk = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return str(self.author)