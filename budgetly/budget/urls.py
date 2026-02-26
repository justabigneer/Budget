from django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    path('setup/', views.setup, name='setup'),
]