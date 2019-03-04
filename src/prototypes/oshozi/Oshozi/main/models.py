from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ImageUploader(models.Model):
  description = models.CharField(max_length = 50)
  image = models.ImageField(upload_to='media/')

  def save(self, *args, **kwargs):
    url = self.image.url
    description = self.description
    img = Image(description= description, url= '/media/' + url)
    img.save() 

  def __str__(self):
    return self.description

  def marshallable(self):
    return{
      'description': self.description,
      'url': self.image.url,
    }

class Image(models.Model):
  description = models.CharField(max_length = 50)
  url = models.CharField(max_length = 50)

  def __str__(self):
    return self.description

  def marshallable(self):
    return{
      'description': self.description,
      'url': self.url,
    }


class Sound(models.Model):
  description= models.CharField(max_length=100)
  # sound_file = FileField(upload_to='sounds', default='sound/default_sound.mp3')

  def __str__(self):
    return self.description

  def marshallable(self):
    return{
      'description': self.description,
    }


class State(models.Model):
  ALARM = 0
  REPOSE = 1
  IGNORED = 2
  TAMPER = 3
  CHORT_CIRCUIT = 4

  name = models.CharField(max_length=50)
  description = models.CharField(max_length=100)
  image = models.ForeignKey(Image, on_delete=models.CASCADE,)
  sound = models.ForeignKey(Sound, on_delete=models.CASCADE,)
  color = models.PositiveSmallIntegerField(
          choices = (
            (ALARM, "ALARMA"),
            (REPOSE, "REPOSO"),
            (IGNORED, "OMITIDO"),
            (TAMPER, "TAMPER"),
            (CHORT_CIRCUIT, "CORTOCIRCUITO"))
  )

  def __str__(self):
    return self.name

  def marshallable(self):
    return {
      'name': self.name,
      'description': self.description,
      'image': self.image.marshallable(),
      'sound': self.sound.marshallable(),
      'color': self.color,
    }

class Event(models.Model):

  timestamp = models.DateTimeField()
  kind = models.CharField(max_length = 10)
  description = models.CharField(max_length = 50)
  location = models.CharField(max_length = 50)
  status = models.ForeignKey(State)

  def get_date(self, timestamp):
    return str(timestamp).split(' ')[0]

  def get_time(self, timestamp):
    return str(timestamp).split(' ')[1].split('+')[0]

  def marshallable(self):
    return {
      'id': self.pk,
      'date': self.get_date(self.timestamp),
      'time': self.get_time(self.timestamp),
      'kind': self.kind,
      'description': self.description,
      'location': self.location,
      'status': self.status.marshallable(),
    }

  def __str__(self):
    retval = str(self.get_date(self.timestamp)) + '-' + str(self.get_time(self.timestamp)) + '-' + str(self.description)
    return retval

class HwController(models.Model):
  address = models.GenericIPAddressField()
  description = models.CharField(max_length=100)
  # max_inputs = models.PositiveSmallIntegerField(default=0)
  # n_inputs = models.PositiveSmallIntegerField(default=0)
  # max_outputs = models.PositiveSmallIntegerField(default=0)
  # n_outputs =  models.PositiveSmallIntegerField(default=0)
  def __str__(self):
    return self.description


class Device(models.Model):
  INPUT = 'INPUT'
  OUTPUT = 'OUTPUT'
  KIND_OF_DEVICE = (
    (INPUT, 'Input device'),
    (OUTPUT, 'Output device'),
    )
  controller = models.ForeignKey(HwController, on_delete=models.CASCADE,)
  description = models.CharField(max_length=100, unique=True)
  mode = models.CharField(max_length=2, choices=KIND_OF_DEVICE, default=INPUT)
  location = models.CharField(max_length=100)

  def __str__(self):
    return self.description



