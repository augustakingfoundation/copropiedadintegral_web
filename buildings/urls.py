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
from buildings.views.roles import MembershipUpdateView
from buildings.views.roles import MembershipDeleteView
from buildings.views.roles import MembershipTransferView
from buildings.views.data_update import DataUpdateView
from buildings.views.data_update import RequestOwnersUpdateView
from buildings.views.data_update import RequestLeaseholdersUpdateView
from buildings.views.data_update import RequestResidentsUpdateView
from buildings.views.data_update import OwnersUpdateForm
from buildings.views.data_update import LeaseholdersUpdateForm
from buildings.views.data_update import ResidentsUpdateForm
from buildings.views.data_update import ResidentsUpdatePost
from buildings.views.data_update import VisitorsUpdatePost
from buildings.views.data_update import VehiclesUpdatePost
from buildings.views.data_update import DomesticWorkersUpdatePost
from buildings.views.data_update import PetsUpdatePost


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
        r'^(?P<pk>\d+)/membresías/$',
        MembershipListView.as_view(),
        name='memberships_list',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/membresías/crear/$',
        MembershipFormView.as_view(),
        name='membership_form',
    ),

    # b_pk = Building id.
    # m_pk = Membership id.
    url(
        r'^(?P<b_pk>\d+)/roles/(?P<m_pk>\d+)/actualizar/$',
        MembershipUpdateView.as_view(),
        name='membership_update',
    ),

    # b_pk = Building id.
    # m_pk = Membership id.
    url(
        r'^(?P<b_pk>\d+)/membresías/(?P<m_pk>\d+)/eliminar/$',
        MembershipDeleteView.as_view(),
        name='membership_delete',
    ),

    # b_pk = Building id.
    # m_pk = Membership id.
    url(
        r'^(?P<b_pk>\d+)/roles/(?P<m_pk>\d+)/transferir/$',
        MembershipTransferView.as_view(),
        name='membership_transfer',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/actualizacion-de-datos/$',
        DataUpdateView.as_view(),
        name='data_update_view',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/actualizacion-de-datos/propietarios/solicitar/$',
        RequestOwnersUpdateView.as_view(),
        name='request_owners_update_view',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/actualizacion-de-datos/arrendatarios/solicitar/$',
        RequestLeaseholdersUpdateView.as_view(),
        name='request_leaseholders_update_view',
    ),

    # pk = Building id.
    url(
        r'^(?P<pk>\d+)/actualizacion-de-datos/residentes/solicitar/$',
        RequestResidentsUpdateView.as_view(),
        name='request_residents_update_view',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update owners form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/propietarios/formulario/$',
        OwnersUpdateForm.as_view(),
        name='owners_update_form',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update leaseholders form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/arrendatarios/formulario/$',
        LeaseholdersUpdateForm.as_view(),
        name='leaseholders_update_form',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update residents form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/residentes/formulario/$',
        ResidentsUpdateForm.as_view(),
        name='residents_update_form',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update residents form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/residentes/post/$',
        ResidentsUpdatePost.as_view(),
        name='residents_update_post',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update visitors form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/visitantes/post/$',
        VisitorsUpdatePost.as_view(),
        name='visitors_update_post',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update vehicles form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/vehiculos/post/$',
        VehiclesUpdatePost.as_view(),
        name='vehicles_update_post',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update domestic workers form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/trabajadores-domesticos/post/$',
        DomesticWorkersUpdatePost.as_view(),
        name='domestic_workers_update_post',
    ),

    # pk = Unit update object id.
    # verify_key = Encrypted key to verify update domestic workers form.
    url(
        r'^(?P<pk>\d+)/(?P<verify_key>[0-9a-zA-Z]{50})/actualizacion-de-datos/mascotas/post/$',
        PetsUpdatePost.as_view(),
        name='pets_update_post',
    ),
]
