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
