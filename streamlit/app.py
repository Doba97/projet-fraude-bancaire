import streamlit as st
import pandas as pd
import random
import requests

# Configuration de la page
st.set_page_config(page_title="Portail Client - Détection de Fraude Bancaire", layout="wide")

# Charger les données
@st.cache_data
def load_data():
    df = pd.read_csv("C:/doba/2/IA/projet deploiement/streamlit/bank.csv")
    return df

data = load_data()

# Récupérer les paramètres d'URL
query_params = st.query_params
transaction_id_from_url = query_params.get("Transaction_id", [None])[0]

# Titre principal
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #4B56D2, #82C3EC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }
    .box {
        display: inline-block;
        background-color: #f1f3f8;
        padding: 10px 15px;
        margin: 8px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 500;
        color: #333;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    }
    .red-button > button {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    .prediction-box {
        margin-top: 20px;
        padding: 20px;
        border-radius: 10px;
        background-color: #fff6f6;
        color: #b22222;
        font-weight: bold;
        font-size: 18px;
        border: 1px solid #ffcccc;
        box-shadow: 2px 2px 8px rgba(255, 0, 0, 0.1);
    }
    </style>
    <h1 class="title">💼 Portail Client - Détection de Fraude Bancaire</h1>
""", unsafe_allow_html=True)

# Section de recherche
st.subheader("🔍 Identifiant Client")
col1, col2 = st.columns([3, 1])

with col1:
    transaction_id = st.text_input("Saisissez le Transaction_ID...", value=transaction_id_from_url or "", key="input_id")

with col2:
    if st.button("Génération aléatoire"):
        transaction_id = random.choice(data['Transaction_ID'].dropna().unique().tolist())
        st.query_params["transaction_id"] = transaction_id

# Trouver l'individu
if transaction_id:
    if transaction_id in data['Transaction_ID'].astype(str).values:
        selected = data[data['Transaction_ID'].astype(str) == transaction_id].iloc[0]

        # Affichage des variables dans des rectangles
        st.markdown("""
            <style>
            .info-box {
                background-color: #f9f9f9;
                color: #333;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 1rem;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
            }
            .info-box i {
                font-size: 1.5rem;
                display: block;
                margin-bottom: 0.5rem;
            }
            </style>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Informations du client")
        box_cols = st.columns(3)
        selected_vars = {
            'ID de transaction': (selected['Transaction_ID'], 'fas fa-receipt'),
            'Montant de la transaction': (selected['Transaction_Amount'], 'fas fa-money-bill-wave'),
            'Mode de paiement': (selected['Payment_Method'], 'fas fa-credit-card'),
            'Localisation': (selected['Location'], 'fas fa-map-marker-alt'),
            'Appareil utilisé': (selected['Device_Used'], 'fas fa-desktop'),
            'Âge du compte': (selected['Account_Age'], 'fas fa-hourglass-half')
        }
        for i, (k, (v, icon)) in enumerate(selected_vars.items()):
            with box_cols[i % 3]:
                st.markdown(f"""
                    <div class='info-box'>
                        <i class='{icon}'></i>
                        <strong>{k}</strong><br>{v}
                    </div>
                """, unsafe_allow_html=True)

        # DataFrame de l'individu
        st.markdown("### 📃 Données complètes")
        st.dataframe(pd.DataFrame(selected).transpose())

        # Bouton de prédiction
        if st.button("Prédire ce client", type="primary", key="predict_existing"):
            # Construire payload et appeler API
            payload = selected.drop("Fraudulent", errors='ignore').to_dict()
            try:
                response = requests.post("https://doba97-projet-fraude.hf.space/predire", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get("probabilite_fraude", "Inconnu")
                    prediction_percent = round(float(prediction) * 100, 2)
                    st.markdown(f"""
                        <div class='prediction-box'>
                            🤖 La probabilité que ce client soit frauduleux est de <strong>{prediction_percent} %</strong>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Erreur API: {response.status_code}")
            except Exception as e:
                st.error(f"Erreur de connexion : {str(e)}")
    else:
        st.warning("Transaction_ID introuvable dans la base.")

# Ajout d'un nouvel individu
st.markdown("---")
st.markdown("## ➕ Ajouter un nouveau client")
with st.form(key="new_user_form"):
    cols = st.columns(3)
    user_id = cols[0].text_input("User_ID")
    amount = cols[1].number_input("Transaction_Amount", min_value=0.0)
    account_age = cols[2].number_input("Account_Age", min_value=0)

    cols2 = st.columns(3)
    device_type = cols2[0].selectbox("Device_Used", ['Tablet', 'Mobile', 'Desktop', 'Unknown Device'])
    transaction_type = cols2[1].selectbox("Transaction_Type", ['ATM Withdrawal', 'Bill Payment', 'POS Payment', 'Bank Transfer', 'Online Purchase'])
    payment_method = cols2[2].selectbox("Payment_Method", ['Debit Card', 'Credit Card', 'UPI', 'Net Banking', 'Invalid Method'])

    n_prev_frauds = st.number_input("Previous_Fraudulent_Transactions", min_value=0)
    nb_24h = st.number_input("Number_of_Transactions_Last_24H", min_value=0)
    time = st.time_input("Time_of_Transaction")

    new_submit = st.form_submit_button("Soumettre et Prédire")

    if new_submit:
        new_data = {
            "User_ID": user_id,
            "Transaction_Amount": amount,
            "Account_Age": account_age,
            "Device_Used": device_type,
            "Transaction_Type": transaction_type,
            "Payment_Method": payment_method,
            "Previous_Fraudulent_Transactions": n_prev_frauds,
            "Number_of_Transactions_Last_24H": nb_24h,
            "Time_of_Transaction": str(time)
        }

        try:
            response = requests.post("https://doba97-projet-fraude.hf.space/predire", json=new_data)
            if response.status_code == 200:
                result = response.json()
                prediction = result.get("prediction", "Inconnu")
                st.markdown(f"""
                    <div class='prediction-box'>
                        🤖 La probabilité que ce client soit frauduleux est de <strong>{prediction} %</strong>
                    </div>
                """, unsafe_allow_html=True)
                st.json(new_data)
            else:
                st.error(f"Erreur API: {response.status_code}")
        except Exception as e:
            st.error(f"Erreur de connexion : {str(e)}")

