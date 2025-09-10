import streamlit as st
from PIL import Image
from logic.rules import assess
from logic.report import create_report

# Seitenkonfiguration
st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon="assets/Logo.png",
    layout="centered"
)

# ---------- Branding: Logo + Titel ----------
st.markdown(
    """
    <div style="text-align:center;">
        <img src="app/assets/Logo.png" alt="Logo" style="width:200px; margin-bottom:15px;">
        <h1>EU AI Act Quick-Check</h1>
        <p style="color:gray;">Vereinfachte Selbstprüfung – keine Rechtsberatung.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------- Eingabefelder ----------
is_ai = st.radio("Ist es ein KI-System?", ["Nein", "Ja"])
use_case = st.selectbox("Einsatzbereich", [
    "Bildung", "HR/Bewerbung", "Kredit/Finanzen",
    "Sicherheit/Überwachung", "Biometrisch",
    "Medizin/Gesundheit", "Sonstiges"
])
sensitive = st.multiselect("Datenarten", [
    "Personenbezogen", "Gesundheit", "Kinder/Jugendliche", "Keine/Anonymisiert"
])
biometric_remote = st.checkbox("Biometrische Fernidentifikation (live/remote)")
auto_scoring = st.checkbox("Automatisierte Bewertung (Aufnahme/HR/Kredit/Noten)")
critical_infra = st.checkbox("Kritische Infrastruktur")
transparency = st.checkbox("Transparenzhinweis vorhanden")
human_oversight = st.checkbox("Menschliche Aufsicht geregelt")
logging = st.checkbox("Protokollierung aktiviert")
genai_label = st.checkbox("GenAI-Inhalte gekennzeichnet")

# ---------- Auswertung ----------
if st.button("Prüfen"):
    result = assess(
        is_ai=(is_ai == "Ja"),
        use_case=use_case,
        sensitive=sensitive,
        biometric_remote=biometric_remote,
        auto_scoring=auto_scoring,
        critical_infra=critical_infra,
        transparency=transparency,
        human_oversight=human_oversight,
        logging=logging,
        genai_label=genai_label
    )

    # Ergebnisanzeige mit farbigem Ampelsystem
    if result['risk'] == "Hoch":
        st.error("🔴 Das System fällt in eine hohe Risikoklasse. Unbedingt rechtliche Beratung und Maßnahmen erforderlich!")
    elif result['risk'] == "Mittel":
        st.warning("🟠 Das System hat mittleres Risiko. Zusätzliche Kontrollen empfohlen.")
    else:
        st.success("🟢 Geringes Risiko. Keine besonderen Maßnahmen erforderlich.")

    st.subheader(f"Ergebnis: {result['risk']}")
    st.write("**Begründung:**", "; ".join(result["reasons"]) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result["tasks"]:
        st.write("•", t)

    # ---------- PDF-Export ----------
    pdf = create_report(result, logo_path="assets/Logo.png")
    st.download_button(
        "📄 Ergebnis als PDF herunterladen",
        data=pdf,
        file_name="EU_AI_Act_QuickCheck.pdf",
        mime="application/pdf"
    )

st.divider()

# ---------- Footer ----------
st.markdown("""
<hr/>
<div style='font-size: 13px; color:#64748B; text-align:center;'>
  © 2025 KN-AI-Solutions · 
  <a href='https://kn-ai-solutions.com/impressum/' target='_blank'>Impressum</a> ·
  <a href='https://kn-ai-solutions.com/datenschutz/' target='_blank'>Datenschutz</a> ·
  Kontakt: <a href='mailto:info@kn-ai-solutions.com'>info@kn-ai-solutions.com</a>
</div>
""", unsafe_allow_html=True)
