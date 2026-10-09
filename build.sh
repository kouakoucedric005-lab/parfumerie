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

echo "--- Déploiement prêt ---"
