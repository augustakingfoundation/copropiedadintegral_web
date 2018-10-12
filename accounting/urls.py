from django.conf.urls import url

from .views import AccountingFormView
from .views import CondoAccountingView
from .views import EconomicActivitiesFormView


urlpatterns = [
    url(
        r'^nueva_contabilidad/(?P<building_id>\d+)/$',
        AccountingFormView.as_view(),
        name='accounting_form',
    ),

    url(
        r'^actividades-económicas/$',
        EconomicActivitiesFormView.as_view(),
        name='economic_activities_form',
    ),

    url(
        r'^contabilidad/(?P<building_id>\d+)/$',
        CondoAccountingView.as_view(),
        name='condo_accounting',
    ),
]
