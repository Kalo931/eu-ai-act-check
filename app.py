import streamlit as st
from PIL import Image
from pathlib import Path

from logic.rules import assess
from logic.report import create_report

# ----------------------------------------
# Hilfsfunktion: Logo finden (unabhängig von Groß/Kleinschreibung)
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
                return Image.open(p), str(p)  # Bild + Pfad zurückgeben
            except Exception:
                continue
    return None, None

# Seitenkonfiguration
_, logo_path = load_logo()
st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon=logo_path if logo_path else None,
    layout="centered"
)

# ---------- Branding: Logo + Titel ----------
col_logo, col_title = st.columns([2, 5])
with col_logo:
    logo_img, _ = load_logo()
    if logo_img:
        st.image(logo_img, use_container_width=True)
    else:
        st.caption(" ")  # Platzhalter

with col_title:
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
<div style='font-size: 13px; color:#64748B;'>
  © 2025 KN-AI-Solutions · <a href='https://deine-domain.de/impressum' target='_blank'>Impressum</a> ·
  <a href='https://deine-domain.de/datenschutz' target='_blank'>Datenschutz</a> ·
  Kontakt: <a href='mailto:info@kn-ai-solutions.com'>info@kn-ai-solutions.com</a>
</div>
""", unsafe_allow_html=True)
