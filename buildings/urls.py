from django.conf.urls import url

from buildings.views.buildings import BuildingDetailView
from buildings.views.buildings import BuildingFormView
from buildings.views.buildings import BuildingUpdateView
from buildings.views.parking_lots import ParkingLotFormView
from buildings.views.parking_lots import ParkingLotUpdateView
from buildings.views.parking_lots import ParkingLotDeleteView
from buildings.views.units import UnitDetailView
from buildings.views.units import UnitFormView
from buildings.views.units import UnitsListView
from buildings.views.units import UnitUpdateView
from buildings.views.vehicles import VehicleFormView


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

    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/vehículos/registrar/$',
        VehicleFormView.as_view(),
        name='vehicle_form',
    ),
]
