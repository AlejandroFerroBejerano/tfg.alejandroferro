from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
import models
from .models import User

# Create your views here.
@login_required(login_url="/login/")
def index(request):
  return render(request, 'index.html')

@login_required(login_url="/login/")
def event_log(request):
	return render(request, 'event_log.html')

#Views od serialized models for her representation in AngularJS
@login_required(login_url="/login/")
def get_dataset(request, dataset):
    model = {'events': models.Event}[dataset]
    objects = [m.marshallable() for m in model.objects.all()]
    data = json.dumps(objects)
    return HttpResponse(data)

@login_required(login_url="/login/")
def profile(request, username):
  msg = ""
  current_user = request.user
  if current_user.username != username:
    msg = 'Only the administrator can access the profile of other users'
  user = User.objects.get(username = current_user.username)
  return render(request, 'profile.html', {'username':user.username, 'msg': msg})

# Login/Logout
from django import forms
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(username = username, password = password)
      print user
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponseRedirect('/')
        else:
          state = "AccDisabled"
          msg = "This account has been disabled, please provide the credentials of another account or contact your system administrator"
          print state
      else:
        state = "BadUsrPass"
        msg = "The username or password provided were incorrect, please enter a valid username and password"
        print state
    else:
        state = "EmptyForm"
        msg = "The username and password fields can not be empty, please provide a valid username and password"
        print state
  else:
    state =''
    msg = ''
    form = LoginForm()
    # return render (request, 'login.html', {'login_form': form})
  context = {'state': state, 'msg': msg, 'login_form': form}
  return render (request, 'login.html', context)

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/')

#API Views
from main.models import Event, Device, HwController
from main.serializers import EventSerializer, DeviceSerializer, HwControllerSerializer
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend


#DEVICE
class DeviceAPIList(generics.ListCreateAPIView):
  queryset = Device.objects.all()
  serializer_class = DeviceSerializer
  filter_backends = (DjangoFilterBackend,)
  filter_fields = ('__all__')

class DeviceAPIDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Device.objects.all()
  serializer_class = DeviceSerializer

#HwCONTROLLER
class HwControllerAPIList(generics.ListCreateAPIView):
  queryset = HwController.objects.all()
  serializer_class = HwControllerSerializer
  filter_backends = (DjangoFilterBackend,)
  filter_fields = ('__all__')

class HwControllerAPIDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = HwController.objects.all()
  serializer_class = HwControllerSerializer


#EVENT
class EventAPIList(generics.ListCreateAPIView):
  queryset = Event.objects.all()
  serializer_class = EventSerializer
  filter_backends = (DjangoFilterBackend,)
  filter_fields = ('__all__')


class EventAPIDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Event.objects.all()
  serializer_class = EventSerializer