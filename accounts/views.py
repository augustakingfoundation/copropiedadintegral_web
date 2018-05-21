from django.conf import settings
from django.contrib import messages
from hashids import Hashids

from django.shortcuts import redirect
from django.views.generic import FormView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import Http404

from accounts.forms import SignUpForm
from accounts.forms import LoginForm
from accounts.models import User
from app.tasks import send_email


class SignupView(FormView):
    form_class = SignUpForm
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

        subject = 'Active su cuenta'

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
            'Hemos enviado un correo electrónico para verificar '
            'su dirección de correo electrónico',
        )

        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')
    prefix = 'login'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)

        print("HOLA")
        return redirect('dashboard')

    def form_invalid(self, form):
        print(form.errors)


class EmailVerificationView(TemplateView):
    template_name = 'accounts/signup/verify_email_confirm.html'

    def get(self, request, *args, **kwargs):
        hashids = Hashids(salt=settings.SECRET_KEY, min_length=50)

        user_id = hashids.decode(kwargs['verify_key'])
        if not user_id:
            raise Http404('Verificación no valida.')

        user = get_object_or_404(User, id=user_id[0])

        context = self.get_context_data(**kwargs)
        context['message'] = 'Su dirección de correo electrónico ha sido verificada.'

        if user.is_verified:
            context['message'] = 'Su cuenta ya ha sido verificada previamente.'
            return self.render_to_response(context)

        user.is_verified = True
        user.save()

        return self.render_to_response(context)
