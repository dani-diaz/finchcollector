import numbers
from tokenize import Number
from turtle import numinput
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# Add the Minion class & list and view function below the imports
class Minion:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, hair, description, eyes):
    self.name = name
    self.hair = hair
    self.description = description
    self.eyes = eyes

minions = [
  Minion('kevin the Minion', 'black', 'usually golf gear', 2),
  Minion('Bob the Minion', 'tortoise shell', 'diluted tortoise shell', 0),
  Minion('Dave the Minion', 'black tripod', '3 legged cat', 4)
]


def home(request):
  return HttpResponse('<h1>My Minions Page</h1>')


def about(request):
  return render(request, 'about.html')

def minions_index(request):
  return render(request, 'minions/index.html', {
    'minions': minions,
  })


# Create your views here.
