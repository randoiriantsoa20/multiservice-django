import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.models import Utilisateur

try:
    user, created = Utilisateur.objects.get_or_create(
        identifiant='admin',
        defaults={'nom_complet': 'Administrateur', 'role_privilege': 'admin'}
    )
    user.set_password('M@nager1')
    user.role_privilege = 'admin'
    user.save()
    print("=== SUCCÈS : Mot de passe de 'admin' mis à jour avec succès ! ===")
except Exception as e:
    print(f"=== ERREUR lors de la mise à jour : {e} ===")
