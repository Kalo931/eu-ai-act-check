# app.py — EU AI Act Quick-Check (Logo groß & zentriert, Ampelanzeige, PDF)

import streamlit as st
from pathlib import Path
from PIL import Image
from logic.rules import assess
from logic.report import create_report

# ----------------------------- Page config -----------------------------------
st.set_page_config(
    page_title="EU AI Act Quick-Check",
    page_icon=None,
    layout="centered"
)

# ----------------------------- Utils -----------------------------------------
def find_logo() -> Path | None:
    """
    Versucht mehrere Dateinamen im Ordner 'assets/'.
    Akzeptiert PNG/JPG, Groß-/Kleinschreibung.
    """
    candidates = [
        "assets/logo.png", "assets/Logo.png",
        "assets/logo.jpg", "assets/Logo.jpg",
        "assets/kn-ai-solutions.png", "assets/KN-AI-Solutions.png"
    ]
    for c in candidates:
        p = Path(c)
        if p.exists() and p.is_file():
            return p
    return None

def show_centered_logo(path: Path, width: int = 520) -> None:
    """Zeigt das Logo mittig und groß an (per Spalten-Zentrierung)."""
    try:
        img = Image.open(path)
        col_l, col_c, col_r = st.columns([1, 3, 1])
        with col_c:
            st.image(img, width=width)
    except Exception:
        # Fallback – kein Blockieren wenn Bild fehlschlägt
        st.caption(" ")

# ----------------------------- Branding --------------------------------------
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

logo_path = find_logo()
if logo_path:
    show_centered_logo(logo_path, width=520)   # << Größe hier anpassen (z.B. 600)
else:
    # Optionaler Hinweis – auskommentieren, wenn du keine Meldung möchtest
    st.info("Hinweis: Kein Logo gefunden. Lege eine Datei **assets/logo.png** an.")

st.markdown(
    """
    <h1 style="text-align:center; margin: 0 0 6px 0;">EU AI Act Quick-Check</h1>
    <p style="text-align:center; color:#6b7280; margin-top:0;">
      Vereinfachte Selbstprüfung – keine Rechtsberatung.
    </p>
    """,
    unsafe_allow_html=True
)

st.write("")

# ----------------------------- Eingaben --------------------------------------
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

# ----------------------------- Auswertung ------------------------------------
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

    risk_text = result.get("risk", "").strip().lower()
    if risk_text.startswith("hoch"):
        color = "#ef4444"  # rot
        label = "🔴 Hohes Risiko"
    elif risk_text.startswith("mittel"):
        color = "#f59e0b"  # gelb/orange
        label = "🟡 Mittleres Risiko"
    else:
        color = "#10b981"  # grün
        label = "🟢 Niedriges Risiko"

    # Ampel-Kreis + Label mittig
    st.markdown(
        f"""
        <div style="text-align:center; margin: 8px 0 18px 0;">
            <div style="width:90px;height:90px;border-radius:50%;
                        background:{color};display:inline-block;"></div>
            <h2 style="color:{color}; margin-top:10px;">{label}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Details
    reasons = result.get("reasons", [])
    tasks = result.get("tasks", [])

    st.write("**Begründung:**", "; ".join(reasons) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in tasks:
        st.write("•", t)

    # PDF
    pdf = create_report(result)
    st.download_button(
        "📄 Ergebnis als PDF herunterladen",
        data=pdf,
        file_name="EU_AI_Act_QuickCheck.pdf",
        mime="application/pdf"
    )

st.divider()

# ----------------------------- Footer ----------------------------------------
st.markdown(
    """
    <hr/>
    <div style='font-size: 13px; color:#64748B; text-align:center;'>
      © 2025 KN-AI-Solutions ·
      <a href='https://kn-ai-solutions.com/impressum/' target='_blank'>Impressum</a> ·
      <a href='https://kn-ai-solutions.com/datenschutz/' target='_blank'>Datenschutz</a> ·
      Kontakt: <a href='mailto:info@kn-ai-solutions.com'>info@kn-ai-solutions.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
