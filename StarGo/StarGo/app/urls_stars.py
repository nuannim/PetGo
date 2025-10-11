from django.urls import path
from django.conf.urls.static import static

from django.conf import settings

from . import views

urlpatterns = [
    path("", views.stars, name="stars"),
    path("<int:celebrities_id>/", views.stars_sortby, name="stars_sortby"),
    path("<int:celebrities_id>/edit/", views.stars_edit, name="stars_edit"),
    path("addnewstar/", views.stars_addnewstar, name="stars_addnewstar"),

    # path("sortby/", views.stars_sortby, name="stars_sortby"),

    # path("sortby/<int:celebrities_id>", views.stars_sortby, name="stars_sortby"),
    # path("api/get_stars_data/", views.get_stars_data, name="get_stars_data"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
