import logging

from django.utils import timezone
from datetime import timedelta
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from buildings.models import UnitDataUpdate


logger = logging.getLogger('huey.consumer')


@db_periodic_task(crontab(hour='2', minute='0'))
def expire_data_update_links():
    """
    Periodic task to close old links to update owners data and
    leaseholders data.
    This task run everydays, and it checks update links with more
    than 30 days of creation.
    """
    for unit_data_object in UnitDataUpdate.objects.filter(
        enable_owners_update=True,
        owners_update_activated_at__lt=timezone.now() - timedelta(days=30)
    ):
        # Disable owners update link.
        unit_data_object.enable_owners_update = False
        unit_data_object.save()

        logger.info('Update owners link successfully disabled')

    for unit_data_object in UnitDataUpdate.objects.filter(
        enable_leaseholders_update=True,
        leaseholders_update_activated_at__lt=timezone.now() - timedelta(days=30)
    ):
        # Disable leaseholders update link.
        unit_data_object.enable_leaseholders_update = False
        unit_data_object.save()

        logger.info('Update leaseholders link successfully disabled')

    for unit_data_object in UnitDataUpdate.objects.filter(
        enable_residents_update=True,
        residents_update_activated_at__lt=timezone.now() - timedelta(days=30)
    ):
        # Disable leaseholders update link.
        unit_data_object.enable_residents_update = False
        unit_data_object.residents_update = False
        unit_data_object.visitors_update = False
        unit_data_object.vehicles_update = False
        unit_data_object.domestic_workers_update = False
        unit_data_object.pets_update = False
        unit_data_object.save()

        logger.info('Update leaseholders link successfully disabled')
