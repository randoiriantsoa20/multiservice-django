from django.contrib import admin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password as django_check_password
from django import forms

# Importation de l'ensemble des modèles métiers
from .models import Operateur, Service, CaJournalier, Depense, Production

Utilisateur = get_user_model()

# --- Formulaire & Site Admin Personnalisés ---
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
                if user.mot_de_passe and django_check_password(password, user.mot_de_passe):
                    self.user_cache = user
                else:
                    raise forms.ValidationError("Identifiant ou mot de passe incorrect.")
            except Utilisateur.DoesNotExist:
                raise forms.ValidationError("Identifiant ou mot de passe incorrect.")

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


# --- ENREGISTREMENT ET CONFIGURATION DE L'ADMIN ---

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id_utilisateur', 'identifiant', 'nom_complet', 'role_privilege')
    search_fields = ('identifiant', 'nom_complet')
    list_filter = ('role_privilege',)


@admin.register(Operateur)
class OperateurAdmin(admin.ModelAdmin):
    list_display = ('id_operateur', 'nom_operateur', 'role_operateur', 'utilisateur')
    search_fields = ('nom_operateur', 'role_operateur')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id_service', 'libelle_service', 'tarif', 'temps_estime_mn')
    search_fields = ('libelle_service',)


@admin.register(CaJournalier)
class CaJournalierAdmin(admin.ModelAdmin):
    list_display = ('date_ca', 'montant_ca')
    search_fields = ('date_ca',)
    date_hierarchy = 'date_ca'


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_depense', 'source_depense', 'libelle', 'montant_virement')
    search_fields = ('libelle', 'source_depense')
    list_filter = ('source_depense', 'date_depense')
    date_hierarchy = 'date_depense'


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('id_production', 'date_production', 'service', 'operateur', 'quantite', 'montant_encaisse')
    search_fields = ('remarques',)
    list_filter = ('service', 'operateur', 'date_production')
    date_hierarchy = 'date_production'
