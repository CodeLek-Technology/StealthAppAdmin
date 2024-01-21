import json
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from StealthApp.forms import AddUserForm

from StealthApp.models import Location, LoginHistorie
from .serializers import LoginHistorySerializer, UserSerializer
from datetime import datetime, timedelta

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics

User = get_user_model()

def index(req):
    context = {
        'users': User.objects.filter(is_staff=False)
    }
    return render(req, "main/index.html", context)

def profile(req, id):
    user = User.objects.filter(pk=id).last()
    timeframe = req.GET['timeframe']

    format = '%Y-%m-%d'
    get_date = datetime.strptime(timeframe, format)
    date_difference = (datetime.today()-get_date).days

    context = {
        'user': user,
        'locations': Location.objects.filter(user=user, date=datetime.now()-timedelta(date_difference)), # To get Yesterday's date set "timedelta(1)"
        'date': timeframe,
    }
    return render(req, "main/profile.html", context)

def login_history(req, id):
    user = User.objects.filter(pk=id).last()
    timeframe = req.GET['timeframe']

    format = '%Y-%m-%d'
    get_date = datetime.strptime(timeframe, format)
    date_difference = (datetime.today()-get_date).days

    context = {
        'user': user,
        'login_history': LoginHistorie.objects.filter(user=user, date=datetime.now()-timedelta(date_difference)),
        'date': timeframe,
    }
    return render(req, "main/login_history.html", context)

def add_user(req):
    form = AddUserForm(req.POST or None, req.FILES or None)

    if req.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/main")

    context = {
        'form': form
    }
    return render(req, "main/add_user.html", context)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer

class LocationViews(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        create_bulk = []
        for iterator in request.data['locations']:
            loc = Location(user= request.user, latitude= iterator['latitude'], longitude= iterator['longitude'])
            create_bulk.append(loc)
        Location.objects.bulk_create(create_bulk)
        return Response({'message': 'Location Uploaded'}, status=status.HTTP_201_CREATED)
    
    def get(self, request, format=None):
        content = {
            'message': 'method is not allowed',
        }
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class LoginHistoryViews(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        loc = LoginHistorySerializer(data={"user": request.user.id, "session_type": "LOGOUT"})
        if loc.is_valid(raise_exception=True):
            loc.save()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter(is_staff=False)
        user = get_object_or_404(queryset, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)