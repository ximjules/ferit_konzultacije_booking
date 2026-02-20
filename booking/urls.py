from django.urls import path
from . import views

urlpatterns = [
	# mentor
	path("mentor/slots/", views.mentor_slots, name="mentor_slots"),
	path("mentor/slots/add/", views.mentor_add_slot, name="mentor_add_slot"),
	# studentske
	path("slots/", views.available_slots, name="available_slots"),
	path("slots/<int:slot_id>/book/", views.book_slot, name="book_slot"),
	# ostalo
	path("", views.home, name="booking_home"),
]
