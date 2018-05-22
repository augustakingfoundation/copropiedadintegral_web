from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class CustomUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())

        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        raise PermissionDenied
