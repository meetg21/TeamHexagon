from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path("stream", views.stream,name='stream'),
    
    path("about", views.about,name='about'),

    path("services", views.services,name='services'),

    path("contact", views.contact,name='contact'),

    path("gen", views.gen,name='gen'),
     
    path("__init__", views.__init__,name='__init__'),

    path("", views.home,name='home'),
    
    path("trial", views.trial,name='trial'),
     
]

    
    

