import streamlit as st
import pandas as pd
from openai import OpenAI

# Configuration API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuration page
st.set_page_config(page_title="Agent IA Référentiel", layout="centered")
st.image("logo.png", width=130)
st.markdown("""
<h2 style='text-align: center; color: #004aad;'>Générateur IA de Référentiel de Compétences</h2>
<p style='text-align: center;'>Automatisez la cartographie des compétences selon les codes ROME</p>
""", unsafe_allow_html=True)

# Chargement des métiers avec mise en cache
@st.cache_data
def load_metiers():
    df = pd.read_csv("base_metiers.csv", encoding="utf-8")
    df["display"] = df["metier_libelle"] + " (" + df["direction"] + ")"
    return df

df_metiers = load_metiers()
metiers_display = df_metiers["display"].tolist()

# Mise en cache du résultat IA
@st.cache_data(show_spinner=False)
def generate_referentiel(metier_final, direction, code_rome):
    prompt = f"""
Tu es expert RH dans le secteur bancaire.

Génère un tableau HTML structuré pour un référentiel de compétences du métier suivant :
- Métier : {metier_final}
- Direction : {direction}
- Code ROME : {code_rome}

Structure le tableau avec les colonnes suivantes :
- Catégorie de Compétences (Techniques, Organisationnelles, Relationnelles, Personnelles)
- Compétence
- Description

Le tableau doit contenir au moins 10 lignes, au format HTML (sans CSS ni style), avec une balise <table> complète.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Plus rapide
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.3,
    )
    return response.choices[0].message.content


# Interface de sélection
selected_display = st.selectbox("Sélectionnez un métier dans la liste", [""] + metiers_display)
custom_input = st.text_input("Ou saisissez un métier personnalisé")

# Bouton de génération
if st.button("🧠 Générer le référentiel"):
    if not selected_display and not custom_input:
        st.warning("Veuillez sélectionner ou saisir un métier.")
    else:
        if custom_input:
            metier_final = custom_input
            direction = "Non spécifiée"
            code_rome = "Non spécifié"
        else:
            row = df_metiers[df_metiers["display"] == selected_display].iloc[0]
            metier_final = row["metier_libelle"]
            direction = row["direction"]
            code_rome = row["code_rome"]

        with st.spinner("Génération IA en cours..."):
            try:
                output = generate_referentiel(metier_final, direction, code_rome)
                st.markdown("### 📋 Référentiel généré")
                st.markdown(output, unsafe_allow_html=True)
                st.download_button("📥 Télécharger", output, file_name=f"{metier_final}_referentiel.html")
            except Exception as e:
                st.error(f"Erreur OpenAI : {str(e)}")
