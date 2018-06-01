from django.conf.urls import url

from .views import BuildingFormView


urlpatterns = [
    url(
        r'^crear/$',
        BuildingFormView.as_view(),
        name='building_create',
    ),
]
