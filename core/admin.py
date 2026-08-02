from django.contrib import admin
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

@admin.register(get_user_model())
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id_utilisateur', 'identifiant', 'nom_complet', 'role_privilege')
    search_fields = ('identifiant', 'nom_complet')
    list_filter = ('role_privilege',)
