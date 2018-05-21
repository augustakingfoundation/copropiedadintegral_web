from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

from app.views import HomeView
from app.views import DashboardView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(
        r'^$',
        HomeView.as_view(),
        name='home',
    ),

    url(
        r'^dashboard/$',
        DashboardView.as_view(),
        name='dashboard',
    ),

    url(
        r'^cuentas/',
        include(
            (
                'accounts.urls',
                'accounts',
            ),
            namespace='acounts'
        )
    ),
]
