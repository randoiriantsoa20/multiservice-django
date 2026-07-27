#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py shell -c "
from core.models import Utilisateur
if not Utilisateur.objects.filter(identifiant='admin').exists():
    user = Utilisateur(identifiant='admin', nom_complet='Administrateur', role_privilege='admin')
    user.set_password('M@nager1')
    user.save()
"
