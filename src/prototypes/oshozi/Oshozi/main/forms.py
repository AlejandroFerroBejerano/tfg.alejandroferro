# coding: utf-8; mode: python

from datetime import datetime
from django import forms

from .models import Event, Device

class DeviceForm(forms.ModelForm):
  class Meta:
    model = Device
    fields = '__all__'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

class LoginForm(forms.Form):
  username = forms.CharField(label = 'Username', max_length=64)
  password = forms.CharField(widget=forms.PasswordInput())
