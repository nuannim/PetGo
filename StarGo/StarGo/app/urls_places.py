from django.urls import path

from . import views

urlpatterns = [
    path("", views.places, name="places"),
    path("<int:places_id>/", views.places_sortby, name="places_sortby"),
    path("addnewplace/", views.places_addnewplace, name="places_addnewplace"),

    # path("sortby/<int:places_id>", views.place_sortby, name="place_sortby"),
]
