# Utils for building app functionalities.


def process_unit_formset(formset, unit):
    """
    Function to process the unit form formsets data.
    Post data for owner formset and for leasehodler data
    is processed by this function.
    """
    for form in formset:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.unit = unit
            instance.save()

            delete = form.cleaned_data['DELETE']

            if delete:
                instance.delete()
