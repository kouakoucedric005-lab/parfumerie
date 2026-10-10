#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- Installation des dépendances ---"
pip install -r requirements.txt

echo "--- Collecte des fichiers statiques ---"
python manage.py collectstatic --no-input

echo "--- Application des migrations de base de données ---"
python manage.py migrate

echo "--- Chargement du catalogue de Collection Privée ---"
python manage.py charger_demo

echo "--- Création du superutilisateur admin (si inexistant) ---"
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('ADMIN_USERNAME', 'admin')
email    = os.environ.get('ADMIN_EMAIL', 'admin@parfumerie.com')
password = os.environ.get('ADMIN_PASSWORD', '')
if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superutilisateur \"{username}\" créé.')
else:
    print(f'Superutilisateur \"{username}\" déjà existant ou mot de passe non défini.')
"

echo "--- Déploiement prêt ---"
