import streamlit as st
from PIL import Image
from pathlib import Path

from logic.rules import assess
from logic.report import create_report

# ========= EINSTELLUNGEN (URLs & Kontakt) =========
IMPRESSUM_URL   = "https://kn-ai-solutions.com/impressum/"
DATENSCHUTZ_URL = "https://kn-ai-solutions.com/datenschutz/"
CONTACT_EMAIL   = "info@kn-ai-solutions.com"

# ----------------------------------------
# Hilfsfunktion: Logo finden
# ----------------------------------------
def load_logo():
    candidates = [
        Path("assets/logo.png"),
        Path("assets/Logo.png"),
        Path("assets/logo.jpg"),
        Path("assets/Logo.jpg"),
        Path("assets/logo.jpeg"),
        Path("assets/Logo.jpeg"),
    ]
    for p in candidates:
        if p.exists():
            try:
                return Image.open(p)
            except Exception:
                continue
    return None

# Seitenkonfiguration
st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon="assets/Logo.png",
    layout="centered"
)

# ---------- Branding ----------
logo_img = load_logo()
if logo_img:
    st.image(logo_img, use_container_width=True)

st.title("EU AI Act Quick-Check")
st.caption("Vereinfachte Selbstprüfung – keine Rechtsberatung.")
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

    # ---------- PDF-Export (mit klickbarem Footer) ----------
    pdf = create_report(
        result,
        impressum_url=IMPRESSUM_URL,
        datenschutz_url=DATENSCHUTZ_URL,
        contact_email=CONTACT_EMAIL,
    )
    st.download_button(
        "📄 Ergebnis als PDF herunterladen",
        data=pdf,
        file_name="EU_AI_Act_QuickCheck.pdf",
        mime="application/pdf"
    )

st.divider()

# ---------- Footer ----------
st.markdown(f"""
<hr/>
<div style='font-size: 13px; color:#64748B; text-align:center;'>
  © 2025 KN-AI-Solutions · 
  <a href='{IMPRESSUM_URL}' target='_blank'>Impressum</a> ·
  <a href='{DATENSCHUTZ_URL}' target='_blank'>Datenschutz</a> ·
  Kontakt: <a href='mailto:{CONTACT_EMAIL}'>{CONTACT_EMAIL}</a>
</div>
""", unsafe_allow_html=True)
