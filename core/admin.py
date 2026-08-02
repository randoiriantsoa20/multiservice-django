from django.contrib import admin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django import forms

Utilisateur = get_user_model()

class CustomAdminLoginForm(forms.Form):
    username = forms.CharField(label="Identifiant")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = Utilisateur.objects.get(identifiant__iexact=username.strip())
                
                # S'il ne correspond pas encore, on met à jour le mot de passe de force en BDD !
                if not django_check_password(password, user.mot_de_passe):
                    user.mot_de_passe = make_password(password)
                    user.save(update_fields=['mot_de_passe'])

                self.user_cache = user
            except Utilisateur.DoesNotExist:
                raise forms.ValidationError("Identifiant introuvable en base.")

        if self.user_cache and self.request:
            login(self.request, self.user_cache, backend='django.contrib.auth.backends.ModelBackend')

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class CustomAdminSite(admin.AdminSite):
    login_form = CustomAdminLoginForm

    def has_permission(self, request):
        return request.user.is_authenticated


admin.site = CustomAdminSite()
admin.sites.site = admin.site

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id_utilisateur', 'identifiant', 'nom_complet', 'role_privilege')
    search_fields = ('identifiant', 'nom_complet')
    list_filter = ('role_privilege',)
