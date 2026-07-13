# 1. Utiliser une image de base Python officielle et légère
FROM python:3.10-slim

# 2. Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. Éviter que Python n'écrive des fichiers .pyc et forcer l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copier d'abord les fichiers de dépendances pour profiter du cache Docker
COPY requirements.txt .

# 5. Installer les dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copier le reste du code source du projet dans le conteneur
COPY . .

# 7. (Optionnel) Exposer le port si votre application est un serveur web (ex: 8000)

EXPOSE 8000

# 8. La commande qui se lance au démarrage du conteneur
# Remplacez "main.py" par le script principal de votre application
CMD ["python", "main.py", "-a"]