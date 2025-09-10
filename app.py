import streamlit as st
from PIL import Image
from logic.rules import assess
from logic.report import create_report

# Seitenkonfiguration
st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon=None,
    layout="centered"
)

# ---------- Branding: Logo + Titel ----------
st.markdown("<br>", unsafe_allow_html=True)  # Abstand nach oben

try:
    logo = Image.open("assets/logo.png")
    st.image(logo, width=400)  # <-- größer: 400px Breite
except Exception:
    st.caption(" ")  # Platzhalter, falls kein Logo vorhanden ist

# Titel mittig unter dem Logo
st.markdown(
    """
    <h1 style='text-align: center;'>EU AI Act Quick-Check</h1>
    <p style='text-align: center; color: grey;'>Vereinfachte Selbstprüfung – keine Rechtsberatung.</p>
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
    st.subheader(f"Ergebnis: {result['risk']}")
    st.write("**Begründung:**", "; ".join(result["reasons"]) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result["tasks"]:
        st.write("•", t)

    # ---------- PDF-Export ----------
    pdf = create_report(result)
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
  © 2025 KN-AI-Solutions · <a href='https://kn-ai-solutions.com/impressum/' target='_blank'>Impressum</a> ·
  <a href='https://kn-ai-solutions.com/datenschutz/' target='_blank'>Datenschutz</a> ·
  Kontakt: <a href='mailto:info@kn-ai-solutions.com'>info@kn-ai-solutions.com</a>
</div>
""", unsafe_allow_html=True)
