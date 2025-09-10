from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import io
import os

def create_report(result):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Logo einbinden (prüft ob Datei existiert)
    logo_path = "assets/Logo.png"
    if os.path.exists(logo_path):
        img = Image(logo_path, width=200, height=60)  # Logo größer darstellen
        elements.append(img)
        elements.append(Spacer(1, 1*cm))

    # Titel
    elements.append(Paragraph("EU AI Act Quick-Check – Ergebnisbericht", styles['Title']))
    elements.append(Spacer(1, 0.5*cm))

    # Ergebnis
    elements.append(Paragraph(f"<b>Ergebnis:</b> {result['risk']}", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    # Begründung
    reasons = "; ".join(result["reasons"]) or "Keine besonderen Risiken festgestellt."
    elements.append(Paragraph(f"<b>Begründung:</b> {reasons}", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    # Nächste Schritte
    elements.append(Paragraph("<b>Nächste Schritte:</b>", styles['Heading3']))
    for t in result["tasks"]:
        elements.append(Paragraph(f"• {t}", styles['Normal']))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
