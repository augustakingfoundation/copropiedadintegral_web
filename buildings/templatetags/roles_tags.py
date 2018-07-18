from django import template

from buildings.permissions import RolesPermissions

register = template.Library()


@register.simple_tag
def get_can_edit_membership(user, membership):
    return RolesPermissions.can_edit_membership(
        user=user,
        membership=membership,
    )
