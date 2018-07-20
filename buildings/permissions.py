from django.db.models import Q

from .models import BuildingMembership
from .data import MEMBERSHIP_TYPE_ADMINISTRATOR
from .data import MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT


class BuildingPermissions(object):
    @classmethod
    def can_create_building(self, user):
        if user.is_active and user.is_verified:
            return True

        return False

    @classmethod
    def can_view_building_detail(self, user, building):
        if BuildingMembership.objects.filter(
            user=user,
            user__is_active=True,
            user__is_verified=True,
            building=building,
            is_active=True,
        ):
            return True
        return False

    @classmethod
    def can_edit_building(self, user, building):
        if BuildingMembership.objects.filter(
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR) |
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT),
            user=user,
            building=building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return True
        return False

    @classmethod
    def can_view_units_list(self, user, building):
        if BuildingMembership.objects.filter(
            user=user,
            building=building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return True
        return False

    @classmethod
    def can_create_unit(self, user, building):
        if BuildingMembership.objects.filter(
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR) |
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT),
            user=user,
            building=building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return True
        return False

    @classmethod
    def can_view_unit_detail(self, user, building):
        if BuildingMembership.objects.filter(
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR) |
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT),
            user=user,
            building=building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return True
        return False

    @classmethod
    def can_edit_unit(self, user, building):
        if BuildingMembership.objects.filter(
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR) |
            Q(membership_type=MEMBERSHIP_TYPE_ADMINISTRATIVE_ASSISTANT),
            user=user,
            building=building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return True
        return False


class RolesPermissions(object):
    @classmethod
    def can_manage_roles(self, user, building):
        if BuildingMembership.objects.filter(
            membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR,
            user=user,
            building=building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return True
        return False

    @classmethod
    def can_edit_membership(self, user, membership):
        # Validate that authenticated user has administrator membership.
        if not BuildingMembership.objects.filter(
            membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR,
            user=user,
            building=membership.building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return False

        # users can't edit their own membership.
        if membership.user == user:
            return False

        # Return True if authenticated user is main administrator.
        # The creator of the building (condo) object is by default
        # the main administrator and has all permission.
        if membership.building.created_by == user:
            return True

        # Only main administrator can edit his own membership.
        if membership.building.created_by == membership.user:
            return False

        return False

    @classmethod
    def can_delete_membership(self, user, membership):
        # Validate that authenticated user has administrator membership.
        if not BuildingMembership.objects.filter(
            membership_type=MEMBERSHIP_TYPE_ADMINISTRATOR,
            user=user,
            building=membership.building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return False

        # Main administrator membership can not be deleted.
        if membership.building.created_by == membership.user:
            return False

        # Main membership can delete all membership types.
        if user == membership.building.created_by:
            return True

        # Common administrators can delete their own membership.
        if user == membership.user:
            return True

        # Common administrators can delete all membership types,
        # excpet administrators memberships, only main administrator
        # can.
        if membership.membership_type != MEMBERSHIP_TYPE_ADMINISTRATOR:
            return True

        return False
