from django.conf.urls import url

from .views import BuildingDetailView
from .views import BuildingFormView
from .views import BuildingUpdateView
from .views import ParkingLotFormView
from .views import ParkingLotUpdateView
from .views import ParkingLotDeleteView
from .views import UnitDetailView
from .views import UnitFormView
from .views import UnitsListView
from .views import UnitUpdateView


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

    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/actualizar/$',
        UnitUpdateView.as_view(),
        name='unit_update',
    ),

    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/parqueaderos/registrar/$',
        ParkingLotFormView.as_view(),
        name='parking_lot_form',
    ),

    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/parqueaderos/actualizar/(?P<p_pk>\d+)/$',
        ParkingLotUpdateView.as_view(),
        name='parking_lot_update',
    ),

    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/parqueaderos/eliminar/(?P<p_pk>\d+)/$',
        ParkingLotDeleteView.as_view(),
        name='parking_lot_delete',
    ),
]
