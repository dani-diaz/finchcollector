from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import uuid
import boto3

from minioncollector.settings import LOGIN_REDIRECT_URL
from .models import Minion, Weapon, Photo
from .forms import FeedingForm


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def minions_index(request):
  minions = Minion.objects.filter(user=request.user)
  return render(request, 'minions/index.html', {'minions': minions})

@login_required
def minions_detail(request, minion_id):
  minion = Minion.objects.get(id=minion_id)
  id_list = minion.weapons.all().values_list('id')
  weapons_minion_doesnt_have = Weapon.objects.exclude(id__in=id_list)
  feeding_form = FeedingForm()
  return render(request, 'minions/detail.html', {
    'minion': minion,
    'feeding_form': feeding_form,
    'weapons': weapons_minion_doesnt_have
  })

class MinionCreate(LoginRequiredMixin, CreateView):
  model = Minion
  fields = ['name', 'type', 'description', 'eyes']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class MinionUpdate(LoginRequiredMixin, UpdateView):
  model = Minion
  fields = ['type', 'description', 'eyes']

class MinionDelete(LoginRequiredMixin, DeleteView):
  model = Minion
  success_url = '/minions/'

@login_required
def add_feeding(request, minion_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.minion_id = minion_id
    new_feeding.save()
  return redirect('detail', minion_id=minion_id)

@login_required
def assoc_weapon(request, minion_id, weapon_id):
  Minion.objects.get(id=minion_id).weapons.add(weapon_id)
  return redirect('detail', minion_id=minion_id)

@login_required
def unassoc_weapon(request, minion_id, weapon_id):
  Minion.objects.get(id=minion_id).weapons.remove(weapon_id)
  return redirect('detail', minion_id=minion_id)

class WeaponList(LoginRequiredMixin, ListView):
  model = Weapon

class WeaponDetail(LoginRequiredMixin, DetailView):
  model = Weapon

class WeaponCreate(LoginRequiredMixin, CreateView):
  model = Weapon
  fields = '__all__'

class WeaponUpdate(LoginRequiredMixin, UpdateView):
  model = Weapon
  fields = ['name', 'color']

class WeaponDelete(LoginRequiredMixin, DeleteView):
  model = Weapon
  success_url = '/weapons/'

@login_required
def add_photo(request, minion_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, minion_id=minion_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', minion_id=minion_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
