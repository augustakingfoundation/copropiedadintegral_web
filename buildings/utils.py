# Utils for building app functionalities.


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
