from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf.urls.i18n import i18n_patterns

from accounts.forms import UserPasswordResetForm
from accounts.views import SignupView
from app.views import DashboardView
from app.views import HomeView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
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
        r'^recuperar-contraseña/$',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/auth/password_reset_form.html',
            form_class=UserPasswordResetForm,
            html_email_template_name='accounts/auth/password_reset_email.html',
        ),
        name='password_reset',
    ),

    url(
        r'^recuperar-contraseña/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('auth_login'),
            post_reset_login=True,
            template_name='accounts/auth/password_reset_confirm.html',
            post_reset_login_backend=(
                'django.contrib.auth.backends.AllowAllUsersModelBackend'
            ),
        ),
        name='password_reset_confirm',
    ),

    url(
        r'^recuperar-contraseña/hecho/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/auth/password_reset_done.html',
        ),
        name='password_reset_done',
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
            namespace='accounts'
        )
    ),

    url(
        r'^copropiedades/',
        include(
            (
                'buildings.urls',
                'buildings',
            ),
            namespace='buildings'
        )
    ),

    url(
        r'^contabilidad/',
        include(
            (
                'accounting.urls',
                'accounting',
            ),
            namespace='accounting'
        )
    ),
)
