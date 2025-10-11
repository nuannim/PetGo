from django.urls import path
from django.conf.urls.static import static

from django.conf import settings

from . import views

urlpatterns = [
    path('', views.sightings, name='sightings'),
    path('<int:sightings_id>/', views.sightings_edit, name='sightings_edit'),

    # * ไม่ได้ใช้แล้ว ใช้ sightings ธรรมดาแทน
    path("addnewsightings/bystars/<int:celebrities_id>", views.sightings_stars, name="sightings_stars"),
    # path("addnewsightings/byplaces/<int:places_id>", views.sightings_places, name="sightings_places"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
