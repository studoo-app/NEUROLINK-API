# NeuroLink API

API FastAPI pour la gestion d'implants NeuroLink et des clés d'authentification associées.

## Fonctionnalités

- Point d'entrée HTTP avec versionnement `/api/v1`
- Route de santé et d'accueil
- Consultation des implants
- Génération, listing et révocation de clés API
- Persistance locale via SQLite

## Stack technique

- Python 3.13+
- FastAPI
- SQLAlchemy
- Uvicorn
- SQLite

## Structure du projet

- `app/` : bootstrap de l'application et configuration
- `core/` : base de données et utilitaires partagés
- `features/auth/` : authentification et gestion des clés API
- `features/hello/` : routes de test et de santé
- `features/implants/` : lecture des implants
- `scripts/` : scripts utilitaires

## Démarrage local

### Avec Docker

#### Utlisation du container en local

```bash
docker compose up --build
```

#### Utilisation de l'image publiée sur DockerHub

Ajouter le service suivant dans votre `docker-compose.yml` :

```yaml
  api:
    image: nours313/neurolink-api:latest
    container_name: neurolink-api
    ports:
      - "8010:8000"
    environment:
      DATABASE_URL: sqlite:///./neurolink_db_docker
    volumes:
      - ./:/app
    command: uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```


L'API est exposée sur `http://localhost:8010`.

La documentation Swagger est disponible sur `http://localhost:8010/docs`.

### Sans Docker

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Configuration

- `DATABASE_URL` : URL de la base SQLite ou autre moteur SQLAlchemy

Par défaut, l'application utilise `sqlite:///./database.db`.

## Endpoints principaux

### Santé

- `GET /api/v1/hello/`
- `GET /api/v1/hello/health`

### Authentification

Ces routes sont protégées par une dépendance d'administration.

- `POST /api/v1/authentification/generate-key`
- `GET /api/v1/authentification/list-keys`
- `DELETE /api/v1/authentification/revoke/{key_id}`

### Implants

Ces routes nécessitent une clé API valide.

- `GET /api/v1/implants/`
- `GET /api/v1/implants/{reference}`

## Rôles des clés API

Les clés API sont associées à un rôle défini dans `core/enums.py` :

- `User` : accès standard aux ressources publiques et utilisateur
- `Admin` : accès aux opérations de gestion, notamment la génération et révocation des clés
- `SuperAdmin` : rôle le plus élevé, réservé aux opérations de supervision avancée

La vérification du rôle est appliquée via les dépendances FastAPI dans `features/auth/dependencies.py`. Par exemple, `require_admin` interdit l'accès si la clé n'a pas le rôle `Admin`.

## Génération de la clé admin

Une clé administrateur peut être générée automatiquement via le script suivant :

```bash
uv run python scripts/create_admin_keys.py
```

Le script crée une clé API avec le rôle `ADMIN`, affiche son `Key ID` et la valeur complète de la clé, puis recommande de la sauvegarder immédiatement.

Exemple de sortie :

```bash
Admin API key created

Key ID : <key_id>
API Key: <api_key>

Save this key now. It will not be displayed again.
```

Cette clé est ensuite utilisée pour accéder aux routes protégées de gestion des clés et de l'administration.

## Notes

- La base est créée au démarrage via SQLAlchemy.
- Le démarrage lance aussi la logique de startup définie dans `app/startup.py`.
