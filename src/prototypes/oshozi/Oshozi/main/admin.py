from django.contrib import admin
from .models import HwController, Device, Event, Image, Sound, State, ImageUploader

# Register your models here.
admin.site.register(HwController)
admin.site.register(Device)
admin.site.register(Event)
admin.site.register(Image)
admin.site.register(ImageUploader)
admin.site.register(Sound)
admin.site.register(State)