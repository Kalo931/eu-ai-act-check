# app.py — zentriertes, großes Logo + Ampel + PDF

import streamlit as st
from pathlib import Path
from logic.rules import assess
from logic.report import create_report

# ---------- Seiteneinstellungen ----------
# Falls dein Logo-Name anders ist, unten im "find_logo()" anpassen
st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon=None,   # optional: setze hier str(find_logo()) falls du ein Favicon willst
    layout="centered"
)

def find_logo():
    """Liefert den existierenden Logopfad (Logo.png oder logo.png) oder None."""
    for p in [Path("assets/Logo.png"), Path("assets/logo.png")]:
        if p.exists():
            return p
    return None

# ---------- Branding: Logo + Titel ----------
logo_path = find_logo()
# Mittels 3-Spalten-Layout das Logo sauber zentrieren
if logo_path:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Breite nach Bedarf anpassen (z. B. 260-320)
        st.image(str(logo_path), width=260)
else:
    st.write("")

st.markdown(
    """
    <h1 style="text-align:center; margin-bottom:0;">EU AI Act Quick-Check</h1>
    <p style="text-align:center; color:#6b7280;">
      Vereinfachte Selbstprüfung – keine Rechtsberatung.
    </p>
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

# ---------- Auswertung & Anzeige ----------
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

    # Ampel-Heading
    if risk.lower().startswith("hoch"):
        st.markdown("## 🔴 Hohes Risiko")
        st.error("Das System fällt in eine hohe Risikoklasse. Unbedingt rechtliche Beratung und Maßnahmen erforderlich!")
    elif risk.lower().startswith("mittel"):
        st.markdown("## 🟡 Mittleres Risiko")
        st.warning("Es bestehen einige Anforderungen. Bitte prüfen Sie die Pflichten nach EU AI Act genauer.")
    else:
        st.markdown("## 🟢 Niedriges Risiko")
        st.info("Das System ist weitgehend unkritisch. Behalten Sie gesetzliche Änderungen im Blick.")

    # Details
    st.write("**Begründung:**", "; ".join(result.get("reasons", [])) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result.get("tasks", []):
        st.write("•", t)

    # ---------- PDF-Export ----------
    pdf = create_report(result)  # report.py findet das Logo selbst
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
<div style='font-size: 13px; color:#64748B; text-align:center;'>
  © 2025 KN-AI-Solutions · 
  <a href='https://kn-ai-solutions.com/impressum/' target='_blank'>Impressum</a> ·
  <a href='https://kn-ai-solutions.com/datenschutz/' target='_blank'>Datenschutz</a> ·
  Kontakt: <a href='mailto:info@kn-ai-solutions.com'>info@kn-ai-solutions.com</a>
</div>
""", unsafe_allow_html=True)
