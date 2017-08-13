from .models import Usuario

class CustomUserAuth(object):

    def authenticate(self, username=None, password=None):
        try:
            user = Usuario.objects.get(email=username)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Usuario.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except Usuario.DoesNotExist:
            return None