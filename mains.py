from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify

# Chargement du modèle XGBoost entraîné
modele = joblib.load('xgboost_fraud_model.pkl')
model_columns = joblib.load('model_columns.pkl')  # Colonnes utilisées à l'entraînement

# Définition du schéma des données d’entrée pour la prédiction de fraude
class DonneesTransaction(BaseModel):
    User_ID: int  # Identifiant unique de l'utilisateur
    Transaction_Amount: float  # Montant de la transaction
    Transaction_Type: str  # Type de transaction (ex: "retrait", "achat")
    Time_of_Transaction: float  # Heure de la transaction (en minutes depuis minuit)
    Device_Used: str  # Appareil utilisé (ex: "mobile", "desktop")
    Location: str  # Lieu de la transaction (ex: "Abidjan")
    Previous_Fraudulent_Transactions: int  # Nombre de fraudes précédentes
    Account_Age: int  # Ancienneté du compte (en mois)
    Number_of_Transactions_Last_24H: int  # Nombre de transactions dans les dernières 24h
    Payment_Method: str  # Méthode de paiement (ex: "carte", "mobile money")

# Création de l’application Flask
app = Flask(__name__)

# Endpoint racine
@app.route("/", methods=["GET"])
def accueil():
    return jsonify({"message": "Bienvenue sur l’API de détection de fraude bancaire."})

# Endpoint de prédiction
@app.route("/predire", methods=["POST"])
def predire():
    if not request.json:
        return jsonify({"erreur": "Aucune donnée JSON reçue"}), 400

    try:
        # Validation et structuration des données reçues
        donnees = DonneesTransaction(**request.json)
        donnees_df = pd.DataFrame([donnees.dict()])

        # Remplacement des valeurs manquantes numériques par la moyenne
        colonnes_numeriques = [
            'Transaction_Amount', 'Time_of_Transaction', 'Previous_Fraudulent_Transactions',
            'Account_Age', 'Number_of_Transactions_Last_24H'
        ]
        for col in colonnes_numeriques:
            if col in donnees_df.columns:
                donnees_df[col] = donnees_df[col].fillna(donnees_df[col].mean())

        # Remplacement des valeurs manquantes catégorielles par 'unknown'
        colonnes_categorielle = ['Transaction_Type', 'Device_Used', 'Location', 'Payment_Method']
        for col in colonnes_categorielle:
            if col in donnees_df.columns:
                donnees_df[col] = donnees_df[col].fillna('unknown')

        # Encodage des variables catégorielles comme à l'entraînement
        donnees_encoded = pd.get_dummies(donnees_df)

        # Ajout des colonnes manquantes
        for col in model_columns:
            if col not in donnees_encoded.columns:
                donnees_encoded[col] = 0

        # Réordonner les colonnes dans le bon ordre
        donnees_encoded = donnees_encoded[model_columns]

        # Prédiction du modèle
        prediction = modele.predict(donnees_encoded)
        proba_fraude = modele.predict_proba(donnees_encoded)[:, 1]

        # Structure des résultats retournés
        resultats = donnees.dict()
        resultats['prediction'] = int(prediction[0])
        resultats['probabilite_fraude'] = float(proba_fraude[0])
        resultats['interpretation'] = "Transaction Frauduleuse" if prediction[0] == 1 else "Transaction Normale"

        return jsonify({"resultats": resultats})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 400

# Lancer l’application
if __name__ == "__main__":
    app.run(debug=True, port=8000)
