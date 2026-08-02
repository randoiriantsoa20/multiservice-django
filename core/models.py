from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password as django_check_password

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('identifiant')
        
        try:
            user = Utilisateur.objects.get(identifiant=username)
            if user and django_check_password(password, user.mot_de_passe):
                return user
        except Utilisateur.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Utilisateur.objects.get(pk=user_id)
        except Utilisateur.DoesNotExist:
            return None
