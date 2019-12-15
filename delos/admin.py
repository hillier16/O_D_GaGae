from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Member)
admin.site.register(Groupschedule)
admin.site.register(Timeschedule)
admin.site.register(Group)
admin.site.register(Survey)