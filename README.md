# Projet de Détection de Fraude Bancaire

Ce projet a pour objectif de concevoir, entraîner et déployer un modèle d'apprentissage automatique pour la détection de fraudes bancaires. Grâce à une interface utilisateur conviviale et à un backend robuste, les utilisateurs peuvent interagir avec le modèle, explorer les transactions et soumettre de nouveaux cas pour prédiction.

## Table des matières
1. [Description](#description)
2. [Technologies](#technologies)
3. [Structure du projet](#structure-du-projet)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [Tests](#tests)
7. [Déploiement](#d%C3%A9ploiement)
8. [Contributeurs](#contributeurs)

## Description

Le projet repose sur un modèle **XGBoost** entraîné à partir de données transactionnelles issues de la banque. Il permet de :
- Analyser les variables clés des transactions (type de paiement, appareil, localisation, etc.)
- Détecter les comportements anormaux indiquant une fraude potentielle
- Proposer une interface utilisateur claire pour la prédiction et la visualisation des résultats

Fonctionnalités principales :
- 🔍 Recherche par `Transaction_ID`
- 🎲 Génération aléatoire d'un client depuis les données locales
- 📋 Affichage stylisé des variables clés (montant, méthode de paiement, localisation, etc.)
- 🧠 Prédiction de la fraude avec probabilité affichée
- 📝 Ajout d’un nouvel individu via un formulaire et affichage immédiat de sa prédiction

## Technologies

- **Python 3.10+**
- **Streamlit** : Interface utilisateur
- **XGBoost** : Modèle de classification
- **FastAPI** : API backend pour la prédiction
- **Pandas**, **NumPy** : Traitement des données
- **Scikit-learn** : Prétraitement, évaluation
- **Docker** : Conteneurisation
- **Hugging Face Spaces** : Déploiement cloud

## Structure du projet

```
projet_fraude/
├── app.py                    # Script principal Streamlit
├── model/
│   ├── xgboost_fraud_model.pkl     # Modèle entraîné
│   ├── model_columns.pkl           # Colonnes utilisées pour le modèle
├── api/
│   └── app.py               # API FastAPI pour les prédictions
├── data/
│   └── bank.csv             # Données transactionnelles
├── Dockerfile               # Fichier de déploiement Docker
├── requirements.txt         # Dépendances Python
└── README.md                # Documentation du projet
```

## Installation

Clonez le dépôt :
```bash
git clone https://github.com/Doba97/projet_fraude.git
cd projet_fraude
```

Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancement de l'application Streamlit
```bash
streamlit run app.py
```

### API FastAPI
```bash
cd api
uvicorn app:app --reload
```

## Tests

- Validation croisée effectuée durant l'entraînement
- Évaluation avec des métriques adaptées aux données déséquilibrées :
  - Precision, Recall, F1-score, ROC-AUC
- Tests manuels via l’interface utilisateur

## Déploiement

- Local : via Streamlit (`app.py`) et FastAPI (`api/app.py`)
- Cloud : déploiement sur Hugging Face Spaces (grâce au Dockerfile)

## Contributeurs

- **SORO DOBA ISSIAKA** — Étudiant en Master Data Science
- Projet académique dans le cadre du cours « Technologies de l’IA »

---
📧 Contact : dobaissiakasoro97@gmail.com | GitHub : [Doba97](https://huggingface.co/Doba97)
