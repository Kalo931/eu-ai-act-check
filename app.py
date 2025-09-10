# app.py — zentriertes, größeres Logo + Quick-Check

import streamlit as st
from pathlib import Path
from logic.rules import assess
from logic.report import create_report

st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon=None,
    layout="centered"
)

def find_logo():
    for p in [Path("assets/Logo.png"), Path("assets/logo.png")]:
        if p.exists():
            return p
    return None

# ---------- Branding: Logo + Titel ----------
st.markdown(
    """
    <div style="text-align: center;">
        <img src="assets/Logo.png" alt="Logo" style="width: 400px; margin-bottom: 20px;">
        <h1>EU AI Act Quick-Check</h1>
        <p style="color: #64748B; font-size:18px;">Vereinfachte Selbstprüfung – keine Rechtsberatung.</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.write("")

# ---------- Eingaben ----------
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

    risk = result.get("risk", "").strip()

    if risk.lower().startswith("hoch"):
        st.markdown("## 🔴 Hohes Risiko")
        st.error("Das System fällt in eine hohe Risikoklasse. Unbedingt rechtliche Beratung und Maßnahmen erforderlich!")
    elif risk.lower().startswith("mittel"):
        st.markdown("## 🟡 Mittleres Risiko")
        st.warning("Es bestehen einige Anforderungen. Bitte prüfen Sie die Pflichten nach EU AI Act genauer.")
    else:
        st.markdown("## 🟢 Niedriges Risiko")
        st.info("Das System ist weitgehend unkritisch. Behalten Sie gesetzliche Änderungen im Blick.")

    st.write("**Begründung:**", "; ".join(result.get("reasons", [])) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result.get("tasks", []):
        st.write("•", t)

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
    - 🟢 **Grün**: Niedriges Risiko  
    - 🟡 **Gelb**: Mittleres Risiko  
    - 🔴 **Rot**: Hohes Risiko
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
""", unsafe_allow_html=True)# app.py — großes, mittiges Logo

import streamlit as st
from pathlib import Path
from logic.rules import assess
from logic.report import create_report

st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon=None,
    layout="centered"
)

def find_logo():
    for p in [Path("assets/Logo.png"), Path("assets/logo.png")]:
        if p.exists():
            return p
    return None

# ---------- Branding ----------
logo_path = find_logo()
if logo_path:
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.image(str(logo_path), width=600)  # << hier Logo deutlich größer (600 px)
    st.markdown("</div>", unsafe_allow_html=True)
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

# ---------- Eingaben ----------
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

    risk = result.get("risk", "").strip()

    if risk.lower().startswith("hoch"):
        st.markdown("## 🔴 Hohes Risiko")
        st.error("Das System fällt in eine hohe Risikoklasse. Unbedingt rechtliche Beratung und Maßnahmen erforderlich!")
    elif risk.lower().startswith("mittel"):
        st.markdown("## 🟡 Mittleres Risiko")
        st.warning("Es bestehen einige Anforderungen. Bitte prüfen Sie die Pflichten nach EU AI Act genauer.")
    else:
        st.markdown("## 🟢 Niedriges Risiko")
        st.info("Das System ist weitgehend unkritisch. Behalten Sie gesetzliche Änderungen im Blick.")

    st.write("**Begründung:**", "; ".join(result.get("reasons", [])) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result.get("tasks", []):
        st.write("•", t)

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
    - 🟢 **Grün**: Niedriges Risiko  
    - 🟡 **Gelb**: Mittleres Risiko  
    - 🔴 **Rot**: Hohes Risiko
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


