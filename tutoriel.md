#  analyse du projet #

1. Docker Compose : Les services sont déclarés mais incomplets. Il manque les volumes pour la configuration de Prometheus (prometheus.yml) et la persistance de Grafana.
2. FastAPI : Le code de base pour le monitoring est présent (/metrics), mais l'endpoint /predict n'incrémente pas le compteur de requêtes. Il manque également le fichier de dépendances et le Dockerfile.
3. Streamlit : L'interface est fonctionnelle mais nécessite aussi un Dockerfile et un fichier de dépendances.
4. Infrastructure : Le fichier de configuration de Prometheus (prometheus.yml) est totalement absent, ce qui empêchera Prometheus de savoir quoi "scraper" (récupérer comme données).

✦ Après analyse complète, le projet est effectivement à un stade embryonnaire. Pour le finaliser conformément aux consignes du README.md, voici le plan
  d'action que je propose :

  1. Finalisation de l'API Backend (FastAPI)
   * Code : Mettre à jour fastapi_app/main.py pour que toutes les requêtes (y compris /predict) soient comptabilisées dans les métriques Prometheus.
   * Dépendances : Créer un fichier pyproject.toml incluant les dépendances nécessaires (fastapi, uvicorn, prometheus-client, psutil, loguru, python-dotenv).
   * Dockerisation : Créer un Dockerfile optimisé utilisant uv pour installer les dépendances et lancer l'API.

  2. Finalisation du Frontend (Streamlit)
   * Dépendances : Créer un fichier pyproject.toml (streamlit, requests, loguru).
   * Dockerisation : Créer un Dockerfile pour lancer l'application Streamlit.

  3. Mise en place de l'Infrastructure Monitoring (Prometheus & Grafana)
   * Configuration Prometheus : Créer un fichier prometheus.yml pour configurer le "scraping" de l'API et de node-exporter (toutes les 5 secondes comme demandé).
   * Docker Compose :
       * Ajouter le montage du fichier prometheus.yml.
       * Ajouter un volume pour la persistance des données Grafana (/var/lib/grafana).
       * Configurer les ports et les réseaux pour assurer la communication entre les conteneurs.

  4. Validation et Tests
   * Lancement de la stack avec docker compose up --build.
   * Tests manuels via le Frontend pour générer des métriques.
   * Vérification de l'exposition des métriques sur http://localhost:8080/metrics.
   * Vérification de la réception des données dans Prometheus (http://localhost:9090).
   * Configuration finale de Grafana (Importation du dashboard ID 1860 et création du dashboard applicatif).

#  Actions #

## prometheus ##
Configuration de Prometheus et mettre à jour le fichier docker-compose.yml pour que l'infrastructure soit prête à accueillir les applications.

- créer un dossier prometheus pour y placer le fichier de configuration prometheus.yml.

## dockerisation de l'API FastAPI. ##
1. Créer le fichier fastapi_app/pyproject.toml avec uv.
2. Créer le fastapi_app/Dockerfile.
3. Mettre à jour fastapi_app/main.py pour inclure le compteur de requêtes sur l'endpoint /predict.
```python
@app.post("/predict")
async def predict(data: str = Form(...)):
    REQUEST_COUNT.labels(method="POST", endpoint="/predict").inc()
    logger.info(f"Donnée reçue : {data}")
    return {"prediction": "Valeur prédite", "value": 450}
```

## streamlit ##
1. Créer streamlit_app/pyproject.toml.
2. Créer streamlit_app/Dockerfile.

## build l application ##
```
docker compose up --build
```

  Une fois lancé, pour finaliser le travail de votre professeur :
   * Allez sur http://localhost:8501 (Streamlit) et envoyez quelques valeurs pour générer des métriques.
   * Allez sur http://localhost:3000 (Grafana), connectez-vous (admin/admin).
   * Ajoutez Prometheus comme source de données (http://prometheus:9090).

        connections > data sources puis add puis selectionner prometheus

   * Importez le dashboard 1860 pour le système.

        dashboard > create  > import a dashboard
        taper 1860 puis load

   * Créez un graphique pour la métrique app_requests_total.

        dasboard > add visualization
        puis metric
        - soit integrer "app_requests_total" (voir le readmme) si il n existe pas 
        - soit aller http://localhost:8501/ et dans metric on voit apparaitre alors "app_requests_total"
        - soit aller http://localhost:8080/ et faire des refrech et cela apparaitre alors "app_requests_total"

# coorections suite au fichier Projet_3_1_Monitoring.md #

liste précise des tâches qu'il vous reste à accomplir, organisées par étapes logiques :

  Étape 1 : Création de l'arborescence manquante
  Il vous manque les dossiers physiques pour les logs et la configuration automatique de Grafana.
   * Dossier logs/ : Créer le dossier à la racine et les fichiers vides api.log et streamlit.log.
   * Dossier grafana/ : Créer toute la structure de "provisioning" :
       * grafana/provisioning/datasources/
       * grafana/provisioning/dashboards/

  Étape 2 : Configuration du Provisioning (Automatisation)
  Plutôt que de tout configurer à la main dans l'interface de Grafana, le professeur demande d'automatiser la connexion.
   * grafana/provisioning/datasources/datasources.yml : Créer ce fichier pour l'auto-connexion à Prometheus.
   * grafana/provisioning/dashboards/dashboards.yml : Créer ce fichier pour que Grafana sache où chercher les fichiers JSON de tableaux de bord.
   * grafana/provisioning/dashboards/system_health.json : (Optionnel mais conseillé) Y placer l'export du dashboard 1860.

  Étape 3 : Documentation du code (Norme Google)
  Le professeur insiste sur la compréhension via la documentation.
   * fastapi_app/main.py : Ajouter les docstrings (format Google) pour chaque fonction et des commentaires sur la logique de Loguru et Prometheus.
   * streamlit_app/app.py : Faire de même pour la partie interface.

  Étape 4 : Mise à jour du docker-compose.yml
  Votre fichier actuel fonctionne mais ne respecte pas les nouvelles contraintes de sécurité et d'optimisation :
   * Limites de ressources : Ajouter les sections deploy avec les limites de RAM (ex: 512M pour l'API) pour ne pas saturer vos 8GB de RAM.
   * Volumes de Logs : Monter le dossier ./logs dans les services api et streamlit.
   * Volumes Grafana : Remplacer ou compléter le volume de données par le volume de provisioning.
   * Réseaux : Harmoniser le nom du réseau (le professeur utilise app_network).

  Étape 5 : Variables d'environnement
   * Vérifier que votre fichier .env contient bien toutes les variables utilisées dans le Compose (FASTAPI_PORT, GRAFANA_PORT, etc.).

## note personnel ##
- Dans @streamlit_app/app.py  tu dans res = requests.post(f"{api_url}/predict", data={"data":
   val}, timeout=5) rajouter timeout=5 a quoi cela sert et est indispensable? peux t on l enlever ?

     C'est une excellente question technique. Le timeout=5 n'est pas strictement indispensable pour que le code fonctionne, mais il est considéré comme une
     bonne pratique (Best Practice) en développement pour trois raisons :

     1. Éviter le blocage (Freeze) : Sans timeout, si votre API (api:8080) plante ou est surchargée, l'interface Streamlit peut rester "bloquée" indéfiniment
          en attendant une réponse qui ne viendra jamais. La petite roue de chargement tournera sans fin, ce qui est frustrant pour l'utilisateur.
     2. Gestion propre des erreurs : Avec timeout=5, si l'API ne répond pas au bout de 5 secondes, une erreur est déclenchée. Grâce au bloc try...except que
          j'ai ajouté, Streamlit affichera un message d'erreur clair à l'utilisateur au lieu de simplement ramer.
     3. Libération des ressources : Cela permet de libérer la connexion réseau et la mémoire si le serveur distant est trop lent.

     Pouvez-vous l'enlever ?
     Oui, vous pouvez tout à fait l'enlever. Le code deviendrait simplement :
     res = requests.post(f"{api_url}/predict", data={"data": val})

     Mon conseil : Gardez-le. C'est le genre de petit détail qui montre à votre professeur que vous avez une approche professionnelle et que vous anticipez les
     problèmes de réseau ou de performance.

- Dans @fastapi_app/main.py tu a s dans logger.add("/logs/api.log", rotation="500 MB", level="INFO",
   backtrace=True, diagnose=True) rajouter level="INFO", backtrace=True, diagnose=True a quoi cela sert ? est ce indispensable ou peut on l enlever ?

   Ces paramètres ne sont pas indispensables pour le fonctionnement du code, mais ils sont extrêmement précieux pour le monitoring et le débogage, ce qui est
  le cœur de votre exercice.

  Voici à quoi ils servent précisément :

   1. level="INFO" : Définit le "seuil" de ce qui est écrit dans le fichier. Seuls les messages importants (INFO, WARNING, ERROR, CRITICAL) seront
      enregistrés. Cela évite de remplir votre disque dur avec des messages de détails techniques inutiles (DEBUG) que Loguru génère parfois.
   2. backtrace=True : Si votre API plante avec une erreur Python, Loguru enregistrera toute la "trace" (l'historique des appels de fonctions) dans le
      fichier de log. C'est indispensable pour savoir exactement où le code a échoué.
   3. diagnose=True : C'est une option "magique" de Loguru. En cas d'erreur, elle affiche la valeur des variables au moment du plantage directement dans le
      log. C'est un gain de temps énorme pour comprendre pourquoi un bug est survenu.

  Peut-on les enlever ?
  Oui, vous pouvez les supprimer et ne garder que :
  logger.add("/logs/api.log", rotation="500 MB")

  Mon conseil : Comme votre projet porte sur le Monitoring, montrer que vous savez configurer un système de logs robuste avec diagnostic intégré est un
  excellent point pour votre évaluation. Je vous suggère de les laisser, car ils vous aideront énormément si vous rencontrez une erreur lors du docker
  compose up.