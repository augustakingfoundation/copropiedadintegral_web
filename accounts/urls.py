from django.conf.urls import url

from .views import EmailVerificationView
from .views import ProfileFormView
from .views import ResendEmailVerificationView
from django.views.generic import TemplateView


urlpatterns = [
    url(
        r'^verificar/(?P<verify_key>[0-9a-zA-Z]{50})/$',
        EmailVerificationView.as_view(),
        name='email_verification',
    ),

    url(
        r'^correo-no-verificado/$',
        TemplateView.as_view(
            template_name='accounts/signup/unverified_email.html',
        ),
        name='unverified_email',
    ),

    url(
        r'^reenviar-correo-de-verificación/$',
        ResendEmailVerificationView.as_view(),
        name='resend_email_verification',
    ),

    url(
        r'^editar-perfil/',
        ProfileFormView.as_view(),
        name='profile_form_view',
    ),
]
