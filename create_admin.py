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
    user.set_password('MonMotDePasse123!')
    user.role_privilege = 'admin'
    user.save()
    print("=== ADMIN USER CREATED / UPDATED SUCCESSFULLY ===")
except Exception as e:
    print(f"=== ERROR CREATING ADMIN USER: {e} ===")
