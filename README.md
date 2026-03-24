# Microservices Monitoring Stack (FastAPI / Streamlit / Prometheus)

Ce dépôt déploie une infrastructure conteneurisée permettant l'exposition, la collecte et la visualisation de métriques applicatives et système. La gestion des dépendances est assurée par **uv** pour garantir des builds rapides et une isolation stricte des environnements.

## Architecture des Composants

### 1. API Backend (FastAPI)

* **Finalité** : Traitement de données et exposition de points de contrôle.
* **Interface** : Propose un point d'entrée pour la réception de données via formulaires.
* **Observabilité** : Le point de terminaison `/metrics` expose l'état interne de l'application (CPU, RAM, compteurs de requêtes) au format OpenMetrics.

### 2. Frontend de Contrôle (Streamlit)

* **Finalité** : Interface de gestion et de test pour l'interaction avec l'API.
* **Connectivité** : Communique exclusivement via le réseau virtuel Docker pour une isolation optimale.

### 3. Collecte & Stockage (Prometheus)

* **Scraping** : Récupère les données de l'API et du **Node Exporter** (métriques hôtes) toutes les 5 secondes.

---

## Adresses Réseaux et Accès

Accès aux services depuis la machine hôte :

| Service | Point d'entrée Local | Point d'entrée Docker |
| --- | --- | --- |
| **API Backend** | `http://localhost:8080` | `http://api:8080` |
| **Interface Frontend** | `http://localhost:8501` | `http://streamlit:8501` |
| **SGBD Metrics (Prometheus)** | `http://localhost:9090` | `http://prometheus:9090` |
| **Dashboard (Grafana)** | `http://localhost:3000` | `http://grafana:3000` |

> **Note** : Un compteur (Counter) Prometheus n'est instancié dans la base de données qu'après son premier incrément. **Il est impératif de solliciter l'API via le Frontend ou la racine (`/`) plusieurs fois** pour que la métrique `app_requests_total` soit référencée par Prometheus.

---

## Configuration de la Visualisation (Grafana)

### 1. Métriques Système (Node Exporter)

L'analyse des ressources matérielles s'effectue via l'import d'un modèle communautaire :

1. **Import** : Menu Dashboards > New > Import.
2. **Identifiant** : Saisir l'ID **1860** (Load).
3. **Source** : Sélectionner **Prometheus**.
*La persistance des données est garantie par les volumes Docker montés sur `/var/lib/grafana`.*

### 2. Métriques Applicatives (FastAPI)

Pour visualiser le flux de requêtes :

1. **Création** : New Dashboard > Add Visualization.
2. **Source** : Prometheus.
3. **Requête (Query)** : Saisir `app_requests_total` pour le cumulatif ou `rate(app_requests_total[1m])` pour le débit par seconde.

---

### Lancement de la stack

Toute modification du `pyproject.toml` ou du code nécessite une reconstruction :

```bash
docker compose up --build

```

### Journalisation

Les logs persistants (gérés par Loguru) sont disponibles dans le répertoire racine `./logs/` pour l'audit et le debug.

---

