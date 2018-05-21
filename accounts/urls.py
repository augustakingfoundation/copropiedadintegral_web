from django.conf.urls import url

from .views import SignupView
from .views import EmailVerificationView


urlpatterns = [
    # API Userprofile
    url(
        r'^crear-cuenta/$',
        SignupView.as_view(),
        name='signup',
    ),

    url(
        r'^verificar/(?P<verify_key>[0-9a-zA-Z]{50})/$',
        EmailVerificationView.as_view(),
        name='email_verification',
    ),
]
