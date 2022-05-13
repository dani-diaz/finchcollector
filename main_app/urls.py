from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('minions/', views.minions_index, name='index'),
  path('minions/<int:minion_id>/', views.minions_detail, name='detail'),
  path('minions/create/', views.MinionCreate.as_view(), name='minions_create'),
  path('minions/<int:pk>/update/', views.MinionUpdate.as_view(), name='minions_update'),
  path('minions/<int:pk>/delete/', views.MinionDelete.as_view(), name='minions_delete'),
  path('minions/<int:minion_id>/add_feeding', views.add_feeding, name='add_feeding'),
  path('minions/<int:minion_id>/add_photo/', views.add_photo, name='add_photo'),
  path('minions/<int:minion_id>/assoc_weapon/<int:weapon_id>/', views.assoc_weapon, name='assoc_weapon'),
  path('minions/<int:minion_id>/unassoc_weapon/<int:weapon_id>/', views.unassoc_weapon, name='unassoc_weapon'),
  path('weapons/', views.WeaponList.as_view(), name='weapons_index'),
  path('weapons/<int:pk>/', views.WeaponDetail.as_view(), name='weapons_detail'),
  path('weapons/create/', views.WeaponCreate.as_view(), name='weapons_create'),
  path('weapons/<int:pk>/update/', views.WeaponUpdate.as_view(), name='weapons_update'),
  path('weapons/<int:pk>/delete/', views.WeaponDelete.as_view(), name='weapons_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]