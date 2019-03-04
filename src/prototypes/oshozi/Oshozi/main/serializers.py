#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

from .models import Event, Device, HwController
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class HwControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HwController
        fields = '__all__'
