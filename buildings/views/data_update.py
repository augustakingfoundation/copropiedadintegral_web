from hashids import Hashids

from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.views.generic import View

from app.mixins import CustomUserMixin
from buildings.forms import ConfirmOwnerUpdateFormSet
from buildings.forms import ConfirmLeaseholderUpdateFormSet
from buildings.forms import ConfirmResidentUpdateFormSet
from buildings.forms import OwnerUpdateFormSet
from buildings.forms import LeaseholderUpdateFormSet
from buildings.models import Building
from buildings.models import Unit
from buildings.models import UnitDataUpdate
from buildings.models import Owner
from buildings.models import Leaseholder
from buildings.permissions import BuildingPermissions
from app.tasks import send_email


class DataUpdateView(CustomUserMixin, TemplateView):
    """
    Template view to manage data update module. Administrators
    and administrative assistants can request for data update
    from owners and leaseholders.
    """
    template_name = 'buildings/administrative/data_update/data_update.html'

    def test_func(self):
        return BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.get_object()
        context['active_units'] = True

        context['confirm_owner_update_formset'] = ConfirmOwnerUpdateFormSet(
            prefix='owner_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        context['confirm_leaseholder_update_formset'] = ConfirmLeaseholderUpdateFormSet(
            prefix='leaseholder_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )


        context['confirm_resident_update_formset'] = ConfirmResidentUpdateFormSet(
            prefix='resident_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        return context


class RequestOwnersUpdateView(CustomUserMixin, View):
    """
    View to manage the post request of the owners update formset.
    """
    def test_func(self):
        return BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        # Get formset post data.
        owner_update_formset = ConfirmOwnerUpdateFormSet(
            self.request.POST,
            prefix='owner_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        for form in owner_update_formset:
            if form.is_valid():
                unit_data_object = form.save(commit=False)

                # Get request value. If True, an email
                # will be sent to the unit registered owners.
                update = form.cleaned_data['update']

                if update and unit_data_object.unit.owner_has_email:
                    # Owners update form must be available.
                    unit_data_object.enable_owners_update = True
                    unit_data_object.owners_update_activated_at = timezone.now()

                    # Generate random string to add security to the
                    # owners update link.
                    key = get_random_string(length=30)
                    # This key is used to decrypt the generated url
                    # to activate the update owners data form.
                    unit_data_object.owners_update_key = key
                    unit_data_object.save()

                    unit = unit_data_object.unit

                    # Filter owners by email value. Only send
                    # email if owners have a registered email.
                    for owner in unit.owner_set.exclude(
                        email__isnull=True,
                    ).exclude(email__exact=''):
                        # Send email.
                        subject = _('Actualizacón de datos de propietarios')

                        update_url = reverse(
                            'buildings:owners_update_form',
                            args=[
                                unit_data_object.id,
                                unit_data_object.owners_data_key,
                            ],
                        )

                        body = render_to_string(
                            'buildings/administrative/data_update/update_email.html', {
                                'title': subject,
                                'owners_update': True,
                                'unit_data_object': unit_data_object,
                                'update_url': update_url,
                                'base_url': settings.BASE_URL,
                            },
                        )

                        send_email(
                            subject=subject,
                            body=body,
                            mail_to=[owner.email],
                        )

        messages.success(
            self.request,
            _('Se ha solicitado la actualización de datos a'
              ' los propietarios con correo electrónico registrado.')
        )

        return redirect(
            'buildings:data_update_view',
            self.get_object().id,
        )


class RequestLeaseholdersUpdateView(CustomUserMixin, View):
    """
    View to manage the post request of the leaseholders update formset.
    """
    def test_func(self):
        return BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        leaseholder_update_formset = ConfirmLeaseholderUpdateFormSet(
            self.request.POST,
            prefix='leaseholder_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        for form in leaseholder_update_formset:
            if form.is_valid():
                unit_data_object = form.save(commit=False)

                # Get update request value. If True, an email
                # will be sent to the unit registered leaseholders.
                update = form.cleaned_data['update']

                if update and unit_data_object.unit.leaseholder_has_email:
                    # Leaseholder update form must be available.
                    unit_data_object.enable_leaseholders_update = True
                    unit_data_object.leaseholders_update_activated_at = timezone.now()

                    # Generate random string to add security to the
                    # leaseholders update link.
                    key = get_random_string(length=30)
                    # This key is used to decrypt the generated url
                    # to activate the update leaseholders data form.
                    unit_data_object.leaseholders_update_key = key
                    unit_data_object.save()

                    unit = unit_data_object.unit

                    # Filter leaseholders by email value. Only send
                    # email if leaseholders have a registered email.
                    for leaseholder in unit.leaseholder_set.exclude(
                        email__isnull=True,
                    ).exclude(email__exact=''):
                        # Send email.
                        subject = _('Actualizacón de datos de arrendatarios')

                        update_url = reverse(
                            'buildings:leaseholders_update_form',
                            args=[
                                unit_data_object.id,
                                unit_data_object.leaseholders_data_key,
                            ],
                        )

                        # Create email content.
                        body = render_to_string(
                            'buildings/administrative/data_update/update_email.html', {
                                'title': subject,
                                'leaseholders_update': True,
                                'unit_data_object': unit_data_object,
                                'update_url': update_url,
                                'base_url': settings.BASE_URL,
                            },
                        )

                        send_email(
                            subject=subject,
                            body=body,
                            mail_to=[leaseholder.email],
                        )

        messages.success(
            self.request,
            _('Se ha solicitado la actualización de datos a'
              ' los arrendatarios con correo electrónico registrado.')
        )

        return redirect(
            'buildings:data_update_view',
            self.get_object().id,
        )


class RequestResidentsUpdateView(CustomUserMixin, View):
    """
    View to manage the post request of the residents  update formset.
    """
    def test_func(self):
        return BuildingPermissions.can_edit_building(
            user=self.request.user,
            building=self.get_object(),
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Building,
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        resident_update_formset = ConfirmResidentUpdateFormSet(
            self.request.POST,
            prefix='resident_update',
            queryset=UnitDataUpdate.objects.filter(
                unit__building=self.get_object(),
            ),
        )

        # for form in resident_update_formset:
        #     if form.is_valid():
        #         unit_data_object = form.save(commit=False)

        #         # Get update request value. If True, an email
        #         # will be sent to the unit registered leaseholders.
        #         update = form.cleaned_data['update']

        #         if update and unit_data_object.unit.leaseholder_has_email:
        #             # Leaseholder update form must be available.
        #             unit_data_object.enable_leaseholders_update = True
        #             unit_data_object.leaseholders_update_activated_at = timezone.now()

        #             # Generate random string to add security to the
        #             # leaseholders update link.
        #             key = get_random_string(length=30)
        #             # This key is used to decrypt the generated url
        #             # to activate the update leaseholders data form.
        #             unit_data_object.leaseholders_update_key = key
        #             unit_data_object.save()

        #             unit = unit_data_object.unit

        #             # Filter leaseholders by email value. Only send
        #             # email if leaseholders have a registered email.
        #             for leaseholder in unit.leaseholder_set.exclude(
        #                 email__isnull=True,
        #             ).exclude(email__exact=''):
        #                 # Send email.
        #                 subject = _('Actualizacón de datos de arrendatarios')

        #                 update_url = reverse(
        #                     'buildings:leaseholders_update_form',
        #                     args=[
        #                         unit_data_object.id,
        #                         unit_data_object.leaseholders_data_key,
        #                     ],
        #                 )

        #                 # Create email content.
        #                 body = render_to_string(
        #                     'buildings/administrative/data_update/update_email.html', {
        #                         'title': subject,
        #                         'leaseholders_update': True,
        #                         'unit_data_object': unit_data_object,
        #                         'update_url': update_url,
        #                         'base_url': settings.BASE_URL,
        #                     },
        #                 )

                        # send_email(
                        #     subject=subject,
                        #     body=body,
                        #     mail_to=[leaseholder.email],
                        # )

        messages.success(
            self.request,
            _('Se ha solicitado la actualización de datos a'
              ' los residentes con correo electrónico registrado.')
        )

        return redirect(
            'buildings:data_update_view',
            self.get_object().id,
        )


class OwnersUpdateForm(TemplateView):
    """
    Owners update form. This form will be available only if
    administrators have enabled the update post by requesting
    owners data update.
    """
    template_name = 'buildings/administrative/data_update/owners_update_form.html'

    def get_object(self, queryset=None):
        unit = get_object_or_404(
            Unit,
            pk=self.kwargs['pk'],
        )

        data_update = unit.unitdataupdate

        # Used hashids library to decrypt the url verify key.
        hashids = Hashids(salt=data_update.owners_update_key, min_length=50)
        verify_key = hashids.decode(self.kwargs['verify_key'])

        # If the decrypted verify key is different to the data update
        # id, the link is corrupt.
        if data_update.id != verify_key[0]:
            raise Http404

        return get_object_or_404(
            UnitDataUpdate,
            enable_owners_update=True,
            pk=verify_key[0],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit_data'] = self.get_object()
        return context

    def get(self, *args, **kwargs):
        owner_update_formset = OwnerUpdateFormSet(
            queryset=Owner.objects.filter(
                unit=self.get_object().unit,
            ),
        )

        return self.render_to_response(
            self.get_context_data(owner_update_formset=owner_update_formset)
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        unit_data_object = self.get_object()
        owner_update_formset = OwnerUpdateFormSet(
            self.request.POST,
            queryset=Owner.objects.filter(
                unit=unit_data_object.unit,
            ),
        )

        if not owner_update_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    owner_update_formset=owner_update_formset,
                )
            )

        # Disable update owners data formset.
        unit_data_object.enable_owners_update = False
        unit_data_object.save()

        for form in owner_update_formset:
            if form.is_valid():
                # Update owner object.
                form.save()

        messages.success(
            self.request,
            _('Gracias por actualizar sus datos.')
        )

        return redirect('home')


class LeaseholdersUpdateForm(TemplateView):
    """
    Leaseholders update form. This form will be available only if
    administrators have enabled the update post by requesting
    leaseholders data update.
    """
    template_name = 'buildings/administrative/data_update/leaseholders_update_form.html'

    def get_object(self, queryset=None):
        unit = get_object_or_404(
            Unit,
            pk=self.kwargs['pk'],
        )

        data_update = unit.unitdataupdate

        # Using hashids library to decrypt the url verify key.
        hashids = Hashids(
            salt=data_update.leaseholders_update_key,
            min_length=50,
        )

        verify_key = hashids.decode(self.kwargs['verify_key'])

        # If the decrypted verify key is different to the data update
        # id, the link is corrupt.
        if data_update.id != verify_key[0]:
            raise Http404

        return get_object_or_404(
            UnitDataUpdate,
            enable_leaseholders_update=True,
            pk=verify_key[0],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit_data'] = self.get_object()
        return context

    def get(self, *args, **kwargs):
        leaseholder_update_formset = LeaseholderUpdateFormSet(
            queryset=Leaseholder.objects.filter(
                unit=self.get_object().unit,
            ),
        )

        return self.render_to_response(
            self.get_context_data(
                leaseholder_update_formset=leaseholder_update_formset,
            )
        )

    @transaction.atomic
    def post(self, *args, **kwargs):
        unit_data_object = self.get_object()
        leaseholder_update_formset = LeaseholderUpdateFormSet(
            self.request.POST,
            queryset=Leaseholder.objects.filter(
                unit=unit_data_object.unit,
            ),
        )

        if not leaseholder_update_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    leaseholder_update_formset=leaseholder_update_formset,
                )
            )

        # Disable update leaseholders data formset.
        unit_data_object.enable_leaseholders_update = False
        unit_data_object.save()

        for form in leaseholder_update_formset:
            if form.is_valid():
                # Update leaseholder object.
                form.save()

        messages.success(
            self.request,
            _('Gracias por actualizar sus datos.')
        )

        return redirect('home')
