from buildings.models import BuildingMembership
from buildings.data import MEMBERSHIP_TYPE_ACCOUNTANT
from buildings.data import MEMBERSHIP_TYPE_ADMINISTRATOR
from buildings.data import MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT


class AccountingPermissions(object):
    @classmethod
    def can_create_accounting(self, user, building):
        if (
            BuildingMembership.objects.filter(
                user=user,
                membership_type__in=(
                    MEMBERSHIP_TYPE_ADMINISTRATOR,
                    MEMBERSHIP_TYPE_ACCOUNTANT,
                ),
                user__is_active=True,
                user__is_verified=True,
                building=building,
                is_active=True,
            )
        ):
            return True

        return False

    @classmethod
    def can_view_accounting_dashboard(self, user, building):
        if not hasattr(building, 'accounting'):
            return False

        if (
            BuildingMembership.objects.filter(
                user=user,
                membership_type__in=(
                    MEMBERSHIP_TYPE_ADMINISTRATOR,
                    MEMBERSHIP_TYPE_ACCOUNTANT,
                    MEMBERSHIP_TYPE_ACCOUNTING_ASSISTANT,
                ),
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
