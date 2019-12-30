from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupSchedule)
admin.site.register(GroupNotice)
admin.site.register(GroupBoard)
admin.site.register(PersonalSchedule)
admin.site.register(TimeTable)
admin.site.register(Alarm)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyAnswer)