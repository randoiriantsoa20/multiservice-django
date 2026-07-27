#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py shell -c "
from core.models import Utilisateur
user, created = Utilisateur.objects.get_or_create(
    identifiant='admin',
    defaults={'nom_complet': 'Administrateur', 'role_privilege': 'admin'}
)
user.set_password('M@nager1')
user.save()
"
