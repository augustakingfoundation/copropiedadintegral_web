from django.conf.urls import url

from .views import BuildingFormView
from .views import BuildingDetailView
from .views import BuildingUpdateView
from .views import UnitsListView
from .views import UnitFormView
from .views import UnitDetailView


urlpatterns = [
    url(
        r'^crear/$',
        BuildingFormView.as_view(),
        name='building_create',
    ),

    url(
        r'^(?P<pk>\d+)/actualizar/$',
        BuildingUpdateView.as_view(),
        name='building_update',
    ),

    url(
        r'^(?P<pk>\d+)/$',
        BuildingDetailView.as_view(),
        name='building_detail',
    ),

    url(
        r'^(?P<pk>\d+)/unidades/$',
        UnitsListView.as_view(),
        name='units_list',
    ),

    url(
        r'^(?P<pk>\d+)/unidades/crear/$',
        UnitFormView.as_view(),
        name='unit_form',
    ),

    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/$',
        UnitDetailView.as_view(),
        name='unit_detail',
    ),
]
