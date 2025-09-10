from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
import io

def create_report(result: dict) -> bytes:
    """
    Erstellt einen PDF-Report mit Logo und Assessment-Ergebnis.
    Gibt ein Byte-Objekt zurück, das Streamlit direkt zum Download anbieten kann.
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # ---------- Logo einfügen ----------
    logo_paths = [
        Path("assets/logo.png"),
        Path("assets/Logo.png"),
        Path("assets/logo.jpg"),
        Path("assets/Logo.jpg"),
    ]
    logo_path = next((p for p in logo_paths if p.exists()), None)
    if logo_path:
        try:
            story.append(Image(str(logo_path), width=150, height=60))  # Größe anpassen
            story.append(Spacer(1, 20))
        except Exception:
            pass  # wenn Bild kaputt, trotzdem weiter machen

    # ---------- Titel ----------
    story.append(Paragraph("EU AI Act Quick-Check", styles["Title"]))
    story.append(Spacer(1, 12))

    # ---------- Ergebnis ----------
    story.append(Paragraph(f"<b>Ergebnis:</b> {result['risk']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # ---------- Begründungen ----------
    story.append(Paragraph("<b>Begründungen:</b>", styles["Heading2"]))
    if result["reasons"]:
        for r in result["reasons"]:
            story.append(Paragraph(f"• {r}", styles["Normal"]))
    else:
        story.append(Paragraph("Keine besonderen Risiken.", styles["Normal"]))
    story.append(Spacer(1, 12))

    # ---------- Aufgaben ----------
    story.append(Paragraph("<b>Nächste Schritte:</b>", styles["Heading2"]))
    for t in result["tasks"]:
        story.append(Paragraph(f"• {t}", styles["Normal"]))

    # ---------- PDF bauen ----------
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
