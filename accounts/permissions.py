class UserPermissions(object):
    @classmethod
    def can_resend_verification_email(self, user):
        if not user.is_verified and user.sent_verification_emails <= 3:
            return True

        return False
