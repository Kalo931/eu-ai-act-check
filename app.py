# app.py  — vollständige Version mit Ampel-Anzeige

import streamlit as st
from PIL import Image
from logic.rules import assess
from logic.report import create_report

# ---------- Seiteneinstellungen ----------
st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon=None,        # Optional: "assets/logo.png"
    layout="centered"
)

# ---------- Branding: Logo + Titel ----------
col_logo, col_title = st.columns([1, 5])

with col_logo:
    try:
        logo = Image.open("assets/Logo.png")  # oder "assets/logo.png" je nach Dateiname
        st.image(logo, use_container_width=False, width=120)
    except Exception:
        st.caption("")

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

# ---------- Auswertung & Anzeige (mit Ampel) ----------
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

    risk = result.get("risk", "").strip()

    # Ampel-Heading + Hinweisboxen
    if risk.lower().startswith("niedrig"):
        st.markdown("## 🟢 Niedriges Risiko")
        st.info("Das System ist weitgehend unkritisch. Behalten Sie gesetzliche Änderungen im Blick.")
    elif risk.lower().startswith("mittel"):
        st.markdown("## 🟡 Mittleres Risiko")
        st.warning("Es bestehen einige Anforderungen. Bitte prüfen Sie die Pflichten nach EU AI Act genauer.")
    else:
        st.markdown("## 🔴 Hohes Risiko")
        st.error("Das System fällt in eine hohe Risikoklasse. Unbedingt rechtliche Beratung und Maßnahmen erforderlich!")

    # Details
    st.write("**Begründung:**", "; ".join(result.get("reasons", [])) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result.get("tasks", []):
        st.write("•", t)

    # PDF-Export (Logo wird in create_report berücksichtigt)
    pdf = create_report(result)
    st.download_button(
        "📄 Ergebnis als PDF herunterladen",
        data=pdf,
        file_name="EU_AI_Act_QuickCheck.pdf",
        mime="application/pdf"
    )

    st.divider()
    st.markdown("""
    ### Ampel-Legende
    - 🟢 **Grün**: Niedriges Risiko – keine oder wenige Vorgaben  
    - 🟡 **Gelb**: Mittleres Risiko – Anforderungen prüfen und ggf. nachrüsten  
    - 🔴 **Rot**: Hohes Risiko – strenge Vorgaben, rechtliche Beratung nötig
    """)

# ---------- Footer ----------
st.markdown("""
<hr/>
<div style='font-size: 13px; color:#64748B;'>
  © 2025 KN-AI-Solutions ·
  <a href='https://kn-ai-solutions.com/impressum/' target='_blank'>Impressum</a> ·
  <a href='https://kn-ai-solutions.com/datenschutz/' target='_blank'>Datenschutz</a> ·
  Kontakt: <a href='mailto:info@kn-ai-solutions.com'>info@kn-ai-solutions.com</a>
</div>
""", unsafe_allow_html=True)

