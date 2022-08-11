# decp-monitoring-v2
Decp-monitoring-v2 a pour objectif de recoder decp-monitoring (https://github.com/139bercy/decp-monitoring) en langage Python.

La procédure est la suivante :

**FACULTATIF**
Si le fichier d'input est un CSV (comme le résultat de decp-augmente par exemple), il faut convertir le csv en json grâce au script csv_to_json après avoir placé je csv dans data/.


**1. ETAPE METADATA**

Afin de réduire la quantité d'informations envoyées sur Github et sur Streamlit, le script json_to_metajson.py permet de réduire l'information présente dans decp.json aux colonnes qui nous intéressent pour produire nos graphiques.

**3. ETAPE STREAMLIT**

Dans le script python Dashboard.py, on spécifie les graphiques et mises en page que l'on souhaite obtenir à partir du decp.json en terme de visualisation.

**4. CI**

Afin que le site streamlit (https://achazryus-decp-monitoring-v2-dashboard-vmy2o6.streamlitapp.com/) soit mis à jour tous les jours, une CI a été mise en place. Celle-ci effectue les étapes suivantes toutes les 24h :
- Déploiement d'une image Dockers (139bercy/decp)
- Récupération des données en ligne via wget
- Exécution du script json_to_metajson.py
- Commit du fichier de données pour que le repo Github porte les données metadata
