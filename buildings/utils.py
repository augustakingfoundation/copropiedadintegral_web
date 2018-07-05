# Utils for building app functionalities.

from django.utils.translation import ugettext as _


def validate_is_main_formset(form, formset, formset_type):
    """
    Function created to validate the 'is main' field in
    owners formset and in leaseholders formset. Only one
    form in the formset must has the 'is_main' input checked.
    """

    # This variable records the number of forms with the
    # 'is_main' field checker.
    is_main_counter = 0

    for formset_form in formset:
        # Get the 'is_main' input value.
        is_main = formset_form.cleaned_data['is_main']

        if is_main:
            # If 'is_main' field is checker, the counter records it.
            is_main_counter += 1

            # If there are more than one form with the 'is_main'
            # checked, an error is added to the current form in
            # the formset.
            if is_main_counter > 1:
                # Add error if there are more than one 'is_main' input checked.
                if formset_type == 'owner':
                    # Error message for owner formset.
                    error = _('La unidad debe tener solo 1'
                              ' propietario principal.')
                elif formset_type == 'leaseholder':
                    # Error message for leaseholder formset.
                    error = _('La unidad debe tener solo 1'
                              ' arrendatario principal.')
                formset_form.add_error(
                    'is_main', error,
                )

    # Units must have one main owner. If there are not owners,
    # an error is added to the unit form. If the formset type is
    # leaseholder, a minimum number of 'is_main' checked inputs is
    # not required.
    if is_main_counter == 0 and formset_type == 'owner':
        form.add_error(
            None, _('Asigne al menos un propietario principal.')
        )

    return (form, formset, is_main_counter)


def process_unit_formset(formset, unit):
    """
    Function to process the unit form formsets data.
    Post data for owner formset and for leasehodler data
    is processed by this function.
    """
    # TODO: Provisionally added to add a main leaseholder
    # and a main owner to the unit. Should be added via
    # form fields. Added only because QA team needs it
    # soon. I will update it next days.
    i = 0
    for form in formset:
        i += 1
        if form.is_valid():
            instance = form.save(commit=False)
            instance.unit = unit

            if i == 1:
                instance.is_main = True

            instance.save()

            delete = form.cleaned_data['DELETE']

            if delete:
                instance.delete()
