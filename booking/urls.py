from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("mentor/slots/", views.mentor_slots, name="mentor_slots"),
    path("mentor/slots/add/", views.mentor_add_slot, name="mentor_add_slot"),
]
