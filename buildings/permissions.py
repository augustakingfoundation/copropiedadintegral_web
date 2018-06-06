from django.db.models import Q

from .models import BuildingMembership


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
            Q(is_administrator=True) |
            Q(is_administrative_assistant=True),
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
            Q(is_administrator=True) |
            Q(is_administrative_assistant=True),
            user=user,
            building=building,
            user__is_active=True,
            user__is_verified=True,
            is_active=True,
        ):
            return True
        return False
