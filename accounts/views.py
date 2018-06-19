from django.conf import settings
from django.contrib import messages
from hashids import Hashids

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View
from django.utils.translation import ugettext as _

from accounts.forms import ProfileForm
from accounts.forms import SignUpForm
from accounts.models import User
from accounts.permissions import UserPermissions
from app.mixins import CustomUserMixin
from app.tasks import send_email


class SignupView(FormView):
    """
    Signup form. User must verify his email.
    """
    form_class = SignUpForm
    template_name = 'accounts/signup/signup.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        user.save()

        subject = _('Active su cuenta')

        body = render_to_string(
            'accounts/signup/verify_email.html', {
                'title': subject,
                'user': user,
                'base_url': settings.BASE_URL,
            },
        )

        send_email(
            subject=subject,
            body=body,
            mail_to=[user.email],
        )

        messages.success(
            self.request,
            _("""Gracias por registrarse.Hemos enviado un
            correo electrónico para verificar su cuenta."""),
        )

        return super().form_valid(form)


class EmailVerificationView(TemplateView):
    """
    Email verification view.
    """
    template_name = 'accounts/signup/verify_email_confirm.html'

    def get(self, request, *args, **kwargs):
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=50)

        user_id = hashids.decode(kwargs['verify_key'])
        if not user_id:
            raise Http404(_('Verificación no valida.'))

        user = get_object_or_404(User, id=user_id[0])

        context = self.get_context_data(**kwargs)
        context['message'] = _('Su dirección de correo electrónico ha sido verificada.')

        if user.is_verified:
            context['message'] = _('Su cuenta ya ha sido verificada previamente.')
            return self.render_to_response(context)

        user.is_verified = True
        user.save()

        return self.render_to_response(context)


class ResendEmailVerificationView(CustomUserMixin, View):
    """
    Unverified accounts can resend a verification email.
    Users only can resend 3 verification email, after that,
    the account is removed. This is to avoid unnecesary
    multiple email sending.
    """
    def test_func(self):
        return UserPermissions.can_resend_verification_email(
            user=self.request.user,
        )

    @transaction.atomic
    def get(self, request, **kwargs):
        user = request.user
        subject = _('Active su cuenta')

        body = render_to_string(
            'accounts/signup/verify_email.html', {
                'title': subject,
                'user': user,
                'base_url': settings.BASE_URL,
            },
        )

        send_email(
            subject=subject,
            body=body,
            mail_to=[user.email],
        )

        user.sent_verification_emails += 1
        user.save()

        messages.success(
            self.request,
            _("""Gracias por registrarse.Hemos enviado un
            'correo electrónico para verificar su cuenta."""),
        )

        return redirect('home')


class ProfileFormView(CustomUserMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('acounts:profile_form_view')

    def test_func(self):
        return UserPermissions.can_edit_profile(
            user=self.request.user,
        )

    def get_object(self):
        return self.request.user

    @transaction.atomic
    def form_valid(self, form):
        form.save()

        messages.success(
            self.request,
            _('Sus datos han sido actualizados correctamente.'),
        )

        return super().form_valid(form)
