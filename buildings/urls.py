from django.conf.urls import url

from .views import BuildingFormView
from .views import BuildingDetailView


urlpatterns = [
    url(
        r'^crear/$',
        BuildingFormView.as_view(),
        name='building_create',
    ),

    url(
        r'^(?P<pk>\d+)/$',
        BuildingDetailView.as_view(),
        name='building_detail',
    ),
]
