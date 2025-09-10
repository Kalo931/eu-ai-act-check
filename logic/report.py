from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def create_report(result: dict) -> bytes:
    """
    Erstellt einen PDF-Report basierend auf dem Ergebnis des Assessments.
    Gibt ein Byte-Objekt zurück, das direkt von Streamlit zum Download angeboten werden kann.
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Titel
    story.append(Paragraph("EU AI Act Quick-Check", styles["Title"]))
    story.append(Spacer(1, 12))

    # Ergebnis
    story.append(Paragraph(f"<b>Ergebnis:</b> {result['risk']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Begründungen
    story.append(Paragraph("<b>Begründungen:</b>", styles["Heading2"]))
    if result["reasons"]:
        for r in result["reasons"]:
            story.append(Paragraph(f"• {r}", styles["Normal"]))
    else:
        story.append(Paragraph("Keine besonderen Risiken.", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Aufgaben
    story.append(Paragraph("<b>Nächste Schritte:</b>", styles["Heading2"]))
    for t in result["tasks"]:
        story.append(Paragraph(f"• {t}", styles["Normal"]))

    # PDF bauen
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
