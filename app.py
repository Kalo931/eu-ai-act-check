import streamlit as st
from logic.rules import assess

st.set_page_config(page_title="EU AI Act Quick-Check", page_icon="✅")
st.title("EU AI Act Quick-Check")
st.caption("Vereinfachte Selbstprüfung – keine Rechtsberatung.")

is_ai = st.radio("Ist es ein KI-System?", ["Nein","Ja"])
use_case = st.selectbox("Einsatzbereich", ["Bildung","HR/Bewerbung","Kredit/Finanzen","Sicherheit/Überwachung","Biometrisch","Medizin/Gesundheit","Sonstiges"])
sensitive = st.multiselect("Datenarten", ["Personenbezogen","Gesundheit","Kinder/Jugendliche","Keine/Anonymisiert"])
biometric_remote = st.checkbox("Biometrische Fernidentifikation (live/remote)")
auto_scoring = st.checkbox("Automatisierte Bewertung (Aufnahme/HR/Kredit/Noten)")
critical_infra = st.checkbox("Kritische Infrastruktur")
transparency = st.checkbox("Transparenzhinweis vorhanden")
human_oversight = st.checkbox("Menschliche Aufsicht geregelt")
logging = st.checkbox("Protokollierung aktiviert")
genai_label = st.checkbox("GenAI-Inhalte gekennzeichnet")

if st.button("Prüfen"):
    result = assess(
        is_ai = (is_ai=="Ja"),
        use_case = use_case,
        sensitive = sensitive,
        biometric_remote = biometric_remote,
        auto_scoring = auto_scoring,
        critical_infra = critical_infra,
        transparency = transparency,
        human_oversight = human_oversight,
        logging = logging,
        genai_label = genai_label
    )
    st.subheader(f"Ergebnis: {result['risk']}")
    st.write("**Begründung:**", "; ".join(result["reasons"]) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result["tasks"]:
        st.write("•", t)

st.divider()
st.caption("© Tolga / Ghost – v0.1")
