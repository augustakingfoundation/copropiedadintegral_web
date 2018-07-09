from django.conf.urls import url

from buildings.views.buildings import BuildingDetailView
from buildings.views.buildings import BuildingFormView
from buildings.views.buildings import BuildingUpdateView
from buildings.views.domestic_workers import DomesticWorkerDeleteView
from buildings.views.domestic_workers import DomesticWorkerFormView
from buildings.views.domestic_workers import DomesticWorkerUpdateView
from buildings.views.parking_lots import ParkingLotDeleteView
from buildings.views.parking_lots import ParkingLotFormView
from buildings.views.parking_lots import ParkingLotUpdateView
from buildings.views.pets import PetDeleteView
from buildings.views.pets import PetDetailView
from buildings.views.pets import PetFormView
from buildings.views.pets import PetUpdateView
from buildings.views.residents import ResidentDeleteView
from buildings.views.residents import ResidentDetailView
from buildings.views.residents import ResidentFormView
from buildings.views.residents import ResidentUpdateView
from buildings.views.units import UnitDeleteView
from buildings.views.units import UnitDetailView
from buildings.views.units import UnitFormView
from buildings.views.units import UnitsListView
from buildings.views.units import UnitUpdateView
from buildings.views.vehicles import VehicleDeleteView
from buildings.views.vehicles import VehicleFormView
from buildings.views.vehicles import VehicleUpdateView
from buildings.views.visitors import VisitorDeleteView
from buildings.views.visitors import VisitorFormView
from buildings.views.visitors import VisitorUpdateView
from buildings.views.roles import MembershipListView
from buildings.views.roles import MembershipFormView


urlpatterns = [
    url(
        r'^crear/$',
        BuildingFormView.as_view(),
        name='building_create',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/actualizar/$',
        BuildingUpdateView.as_view(),
        name='building_update',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/$',
        BuildingDetailView.as_view(),
        name='building_detail',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/unidades/$',
        UnitsListView.as_view(),
        name='units_list',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/unidades/crear/$',
        UnitFormView.as_view(),
        name='unit_form',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/$',
        UnitDetailView.as_view(),
        name='unit_detail',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/actualizar/$',
        UnitUpdateView.as_view(),
        name='unit_update',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/eliminar/$',
        UnitDeleteView.as_view(),
        name='unit_delete',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/parqueaderos/registrar/$',
        ParkingLotFormView.as_view(),
        name='parking_lot_form',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # p_pk = Parking lot id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/parqueaderos/actualizar/(?P<p_pk>\d+)/$',
        ParkingLotUpdateView.as_view(),
        name='parking_lot_update',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # p_pk = Parking lot id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/parqueaderos/eliminar/(?P<p_pk>\d+)/$',
        ParkingLotDeleteView.as_view(),
        name='parking_lot_delete',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/vehículos/registrar/$',
        VehicleFormView.as_view(),
        name='vehicle_form',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # v_pk = Vehicle id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/vehículos/actualizar/(?P<v_pk>\d+)/$',
        VehicleUpdateView.as_view(),
        name='vehicle_update',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # v_pk = Vehicle id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/vehículos/eliminar/(?P<v_pk>\d+)/$',
        VehicleDeleteView.as_view(),
        name='vehicle_delete',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/trabajadores-domésticos/registrar/$',
        DomesticWorkerFormView.as_view(),
        name='domestic_worker_form',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # dm_pk = Domestic worker id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/trabajadores-domésticos/actualizar/(?P<dw_pk>\d+)/$',
        DomesticWorkerUpdateView.as_view(),
        name='domestic_worker_update',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # dm_pk = Domestic worker id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/trabajadores-domésticos/eliminar/(?P<dw_pk>\d+)/$',
        DomesticWorkerDeleteView.as_view(),
        name='domestic_worker_delete',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/mascotas/registrar/$',
        PetFormView.as_view(),
        name='pet_form',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # pet_pk = Pet id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/mascotas/detalle/(?P<pet_pk>\d+)/$',
        PetDetailView.as_view(),
        name='pet_detail',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # pet_pk = Pet id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/mascotas/actualizar/(?P<pet_pk>\d+)/$',
        PetUpdateView.as_view(),
        name='pet_update',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # pet_pk = Pet id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/mascotas/eliminar/(?P<pet_pk>\d+)/$',
        PetDeleteView.as_view(),
        name='pet_delete',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/visitantes-autorizados/registrar/$',
        VisitorFormView.as_view(),
        name='visitor_form',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # av_pk = Authorized visitor id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/visitantes-autorizados/actualizar/(?P<av_pk>\d+)/$',
        VisitorUpdateView.as_view(),
        name='visitor_update',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # av_pk = Authorized visitor id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/visitantes-autorizados/eliminar/(?P<av_pk>\d+)/$',
        VisitorDeleteView.as_view(),
        name='visitor_delete',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/residentes/registrar/$',
        ResidentFormView.as_view(),
        name='resident_form',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # r_pk = Resident id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/residentes/detalle/(?P<r_pk>\d+)/$',
        ResidentDetailView.as_view(),
        name='resident_detail',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # r_pk = Resident id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/residentes/actualizar/(?P<r_pk>\d+)/$',
        ResidentUpdateView.as_view(),
        name='resident_update',
    ),

    # b_pk = Building id.
    # u_pk = unit id.
    # r_pk = Resident id.
    url(
        r'^(?P<b_pk>\d+)/unidades/(?P<u_pk>\d+)/residentes/eliminar/(?P<r_pk>\d+)/$',
        ResidentDeleteView.as_view(),
        name='resident_delete',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/roles/$',
        MembershipListView.as_view(),
        name='memberships_list',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/roles/crear/$',
        MembershipFormView.as_view(),
        name='membership_form',
    ),
]
