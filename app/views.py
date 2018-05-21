from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.views.generic import FormView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import login

from accounts.forms import SignUpForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['signup_form'] = SignUpForm

        return context


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

        user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password2'],
        )
        login(self.request, user)

        messages.success(
            self.request,
            'Hemos enviado un correo electrónico para verificar '
            'su dirección de correo electrónico',
        )
        return super().form_valid(form)
