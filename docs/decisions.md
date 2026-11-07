# Décisions techniques

1. **Sources** : exports CSV de Bank Al-Maghrib. L'API est reportée (évolution possible, même schéma raw).
2. **Raw en TEXT** : aucune perte, aucune rupture si le format change ; nettoyage en staging.
3. **Cours de référence en format long dès l'ingestion** : les dates sont des colonnes variables dans le fichier source.
4. **NUMERIC pour les montants et taux** : précision exacte, pas de FLOAT.