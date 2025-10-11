from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),

    path("", views.profile, name="profile"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path("changepassword/", views.profile_changepassword, name="profile_changepassword"),
    path('deleteaccount/', views.profile_deleteaccount, name='profile_deleteaccount'),

    path('<str:username>/', views.profile_share, name='profile_share'),
]
