from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *

# Create your views here.
def home(request):
    return render(request, 'delos/home.html', {})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer