from django.urls import path
from . import views

urlpatterns = [
    # get
    path('images/', views.list_images, name='list_images'),

    # post
    path('images/upload/', views.upload_image, name='upload_image'),

    # get
    path('images/<str:filename>/', views.get_image, name='get_image'),

    # get
    path('images/<str:filename>/download/', views.download_image_by_filename, name='download_image_by_filename'),
    
    # delete
    path('images/<str:filename>/delete/', views.delete_image, name='delete_image'),
]
