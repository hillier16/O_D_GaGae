from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Groupschedule)
admin.site.register(GroupNotice)
admin.site.register(GroupBoard)
admin.site.register(Timeschedule)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyAnswer)