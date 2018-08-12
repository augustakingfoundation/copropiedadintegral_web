from buildings.models import BuildingMembership
from buildings.data import MEMBERSHIP_TYPE_ACCOUNTANT


class AccountingPermissions(object):
    @classmethod
    def can_create_accounting(self, user, building):
        if (
            user.is_superuser or
            BuildingMembership.objects.filter(
                user=user,
                membership_type=MEMBERSHIP_TYPE_ACCOUNTANT,
                user__is_active=True,
                user__is_verified=True,
                building=building,
                is_active=True,
            )
        ):
            return True

        return False

    @classmethod
    def can_change_economic_activities(self, user):
        if user.is_superuser:
            return True

        return False
