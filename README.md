# Projet de Prédiction de Disponibilité des V'Lille

Ce projet a pour but de prédire la disponibilité des vélos en libre-service (V'Lille) de la métropole lilloise.

## Architecture

Le projet est un monorepo qui contient plusieurs services :

-   `data-ingestion`: Contient les micro-services serverless (AWS Lambda) pour l'ingestion des données.
-   `data-science`: Carnets Jupyter pour l'exploration des données et l'entraînement des modèles.
-   `api`: Une API (FastAPI) pour servir les prédictions du modèle.
-   `frontend`: Une interface web pour visualiser les données et les prédictions.

### Focus : Lambda d'ingestion V'Lille

Le premier service développé est une fonction AWS Lambda située dans `data-ingestion/vlille`.

#### Structure du code

-   `src/main.py`: Le code source de la fonction Lambda.
-   `tests/test_main.py`: Les tests unitaires pour la fonction.

## Intégration et Déploiement Continus (CI/CD)

Le projet utilise les GitHub Actions pour automatiser les tests et les déploiements.

1.  **Tests sur Pull Request** (`.github/workflows/test-vlille-lambda.yml`):
    À chaque pull request qui modifie le code de la lambda, les tests unitaires sont automatiquement exécutés pour garantir la non-régression.

2.  **Déploiement sur `main`** (`.github/workflows/deploy-vlille-lambda.yml`):
    Lorsqu'une modification est poussée sur la branche `main`, le workflow exécute d'abord les tests. S'ils réussissent, il déploie automatiquement une nouvelle version de la fonction Lambda sur AWS.

## Comment commencer ?

### Prérequis

-   Python 3.9+
-   Un compte AWS avec des identifiants configurés

### Lancer les tests localement

1.  Créez et activez un environnement virtuel :
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  Installez les dépendances de test :
    ```bash
    pip install pytest psycopg2-binary
    ```

3.  Lancez les tests :
    ```bash
    PYTHONPATH=data-ingestion/vlille pytest data-ingestion/vlille/tests/
    ```
