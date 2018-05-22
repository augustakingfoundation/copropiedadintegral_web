from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app.views import HomeView
from app.views import DashboardView
from accounts.views import SignupView

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
        r'^crear-cuenta/$',
        SignupView.as_view(),
        name='signup',
    ),

    url(
        r'^iniciar-sesión/$',
        auth_views.login,
        {
            'template_name': 'accounts/auth/login.html',
            'redirect_authenticated_user': True,
        },
        name='auth_login',
    ),


    url(
        r'^cerrar-sesión/$',
        auth_views.LogoutView.as_view(),
        name='logout',
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
