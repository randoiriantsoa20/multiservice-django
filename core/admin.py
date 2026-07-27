from django.contrib import admin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id_utilisateur', 'identifiant', 'nom_complet', 'role_privilege', 'date_creation')
    search_fields = ('identifiant', 'nom_complet')
    list_filter = ('role_privilege',)
