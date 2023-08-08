# from django.urls import path
from .views import home, trigger_emails

from django.urls import path

urlpatterns = [

    path('trigger-emails/',trigger_emails),
    path('home/', home, name='home'),
]