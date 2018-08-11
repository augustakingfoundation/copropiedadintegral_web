from django.conf.urls import url

from .views import AccountingFormView


urlpatterns = [
    url(
        r'^nueva_contabilidad/(?P<building_id>\d+)/',
        AccountingFormView.as_view(),
        name='accounting_form',
    ),
]
