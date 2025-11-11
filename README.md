# ABC KPI Platform (Sample Implementation)

Cette implémentation fournit une version simplifiée de la plateforme d'analytics
présentée sur le site ABC KPI. Elle permet de charger des transactions marketing,
de calculer un ensemble d'indicateurs clés de performance (KPI) et de générer un
rapport texte.

## Fonctionnalités

- Chargement de données CSV avec validation du schéma.
- Calcul automatisé de KPI standards (revenu total, nombre de commandes,
taux de conversion, panier moyen...).
- Segmentation des KPI par dimension (canal, campagne, produit, etc.).
- Interface en ligne de commande pour produire un rapport instantané.
- Tableau de bord React moderne pour explorer les KPI en quelques clics.

## Prise en main rapide

1. Créez (ou utilisez) un fichier CSV conforme au schéma suivant :

   ```csv
   date,revenue,leads,orders,channel,campaign,product
   2024-01-01,1250.50,120,24,Email,Winter Blast,Analytics Suite
   ```

   Un fichier d'exemple est disponible dans `data/sample_transactions.csv`.

2. Exécutez la CLI :

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   python main.py data/sample_transactions.csv --dimension channel
   ```

3. Résultat attendu :

   ```
   === KPI SUMMARY ===
   - Total Revenue: 13 358.55 € — Sum of revenue across all transactions.
   - Orders: 266.00 orders — Total number of orders.
   - Leads: 1 330.00 leads — Total marketing leads captured.
   - Conversion Rate: 20.00 % — Orders divided by leads.
   - Average Order Value: 50.22 € — Revenue divided by number of orders.
   - Revenue per Lead: 10.04 € — Revenue divided by number of leads.

   ## Ads
   === KPI SUMMARY ===
   ...
   ```

## Interface web (React)

Une application React est fournie dans le dossier `frontend/`. Elle propose :

- un sélecteur de dimension (canal, campagne, produit) pour segmenter les KPI ;
- des filtres multi-sélection par canal, campagne et produit ;
- une visualisation sous forme de cartes KPI et de tableau comparatif par segment ;
- l'accès aux données brutes pour export rapide.

### Lancer le tableau de bord

```bash
cd frontend
npm install
npm run dev
```

L'application est servie par Vite sur [http://localhost:5173](http://localhost:5173).

## Structure du projet

- `abckpi_platform/` : cœurs de modules (chargement, calcul, reporting).
- `frontend/` : application React (Vite) pour l'interface web.
- `main.py` : interface CLI.
- `data/` : exemples de données.
- `snake.py` : mini-jeu conservé comme exemple historique.

## Tests

Aucun test automatisé n'est fourni, mais la CLI peut être exécutée avec votre
propre fichier CSV pour valider les calculs.
