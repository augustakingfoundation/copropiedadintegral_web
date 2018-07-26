from django import template

from buildings.permissions import RolesPermissions

register = template.Library()


@register.simple_tag
def get_can_manage_roles(user, building):
    return RolesPermissions.can_manage_roles(
        user=user,
        building=building,
    )


@register.simple_tag
def get_can_edit_membership(user, membership):
    return RolesPermissions.can_edit_membership(
        user=user,
        membership=membership,
    )


@register.simple_tag
def get_can_delete_membership(user, membership):
    return RolesPermissions.can_delete_membership(
        user=user,
        membership=membership,
    )


@register.simple_tag
def get_can_transfer_membership(user, membership):
    return RolesPermissions.can_transfer_membership(
        user=user,
        membership=membership,
    )
