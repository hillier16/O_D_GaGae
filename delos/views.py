from django.shortcuts import render

from rest_framework import viewsets

from .models import *
from .serializers import *

# Create your views here.
def home(request):
    return render(request, 'delos/home.html', {})


class PersonalScheduleViewSet(viewsets.ModelViewSet):
    queryset = PersonalSchedule.objects.all()
    serializers_class = PersonalScheduleSerializer