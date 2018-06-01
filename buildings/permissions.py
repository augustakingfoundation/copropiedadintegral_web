class BuildingPermissions(object):
    @classmethod
    def can_create_building(self, user):
        if user.is_active and user.is_verified:
            return True

        return False
