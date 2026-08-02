from django.contrib import admin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password as django_check_password
from django import forms

# Importation des modèles métiers depuis models.py
from .models import Service, Transaction, CaisseJournaliere

Utilisateur = get_user_model()

# --- Configuration du Formulaire & du Site Admin ---
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


# --- Enregistrement des Modèles dans l'Admin ---

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id_utilisateur', 'identifiant', 'nom_complet', 'role_privilege')
    search_fields = ('identifiant', 'nom_complet')
    list_filter = ('role_privilege',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id_service', 'nom_service', 'tarif_base', 'est_actif')
    search_fields = ('nom_service',)
    list_filter = ('est_actif',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id_transaction', 'date_heure', 'service', 'utilisateur', 'montant', 'mode_paiement')
    search_fields = ('id_transaction', 'remarques')
    list_filter = ('mode_paiement', 'date_heure', 'service')
    date_hierarchy = 'date_heure'  # Navigation rapide par calendrier/date


@admin.register(CaisseJournaliere)
class CaisseJournaliereAdmin(admin.ModelAdmin):
    list_display = ('date_jour', 'fond_de_caisse', 'total_entrees', 'total_sorties', 'solde_final', 'est_cloturee')
    list_filter = ('est_cloturee', 'date_jour')
    date_hierarchy = 'date_jour'
