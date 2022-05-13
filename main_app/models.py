from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

MEALS = (
  ('B', 'Breakfast'),
  ('L', 'Lunch'),
  ('D', 'Dinner'),
)

class Weapon(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('weapons_detail', kwargs={'pk': self.id})

class Minion(models.Model):

  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  eyes = models.IntegerField()
  weapons = models.ManyToManyField(Weapon)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'minion_id': self.id})
  
  def fed_for_today(self):
    return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)  

class Feeding(models.Model):
  date = models.DateField('Feeding Date')
  meal = models.CharField(
    max_length=1,
    choices=MEALS,
    default=MEALS[0][0]
  )
  
  minion = models.ForeignKey(
    Minion,
    on_delete=models.CASCADE
  )

  class Meta:
    ordering = ['-date']

  def __str__(self):
    return f'{self.get_meal_display()} on {self.date}'

class Photo(models.Model):
  url = models.CharField(max_length=200)
  minion = models.ForeignKey(Minion, on_delete=models.CASCADE)

  def __str__(self):
    return f'Photo for minion_id: {self.minion_id} @ {self.url}'