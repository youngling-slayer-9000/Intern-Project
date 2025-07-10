from django.urls import path
from .views import homePage

app_name = 'homeSystem'

urlpatterns = [
    path('', homePage, name='home'),
]