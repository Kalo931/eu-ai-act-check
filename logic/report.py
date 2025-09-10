# logic/report.py — PDF-Erzeugung ohne Logo-Verzerrung

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import io
import os
from PIL import Image as PILImage

def _logo_image_flowable(path: str, target_width_cm: float = 8.0):
    """
    Lädt ein Bild, berechnet proportional die Höhe zu target_width_cm
    und liefert ein reportlab-Image Flowable zurück.
    """
    if not os.path.exists(path):
        return None
    try:
        with PILImage.open(path) as im:
            w, h = im.size
            if w == 0 or h == 0:
                return None
            target_w = target_width_cm * cm
            target_h = target_w * (h / w)  # Seitenverhältnis beibehalten
        return Image(path, width=target_w, height=target_h)
    except Exception:
        return None

def create_report(result: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    # Logo (breit, ohne Verzerrung)
    logo_path = "assets/Logo.png"   # ggf. auf "assets/logo.png" anpassen
    logo = _logo_image_flowable(logo_path, target_width_cm=10.0)  # ca. 10 cm breit
    if logo:
        elements.append(logo)
        elements.append(Spacer(1, 1*cm))

    # Titel
    elements.append(Paragraph("EU AI Act Quick-Check – Ergebnisbericht", styles['Title']))
    elements.append(Spacer(1, 0.6*cm))

    # Ergebnis (Ampeltext)
    risk = result.get("risk", "—")
    elements.append(Paragraph(f"<b>Ergebnis:</b> {risk}", styles['Normal']))
    elements.append(Spacer(1, 0.4*cm))

    # Begründung
    reasons = "; ".join(result.get("reasons", [])) or "Keine besonderen Risiken festgestellt."
    elements.append(Paragraph(f"<b>Begründung:</b> {reasons}", styles['Normal']))
    elements.append(Spacer(1, 0.4*cm))

    # Nächste Schritte
    elements.append(Paragraph("<b>Nächste Schritte:</b>", styles['Heading3']))
    tasks = result.get("tasks", [])
    if tasks:
        for t in tasks:
            elements.append(Paragraph(f"• {t}", styles['Normal']))
    else:
        elements.append(Paragraph("—", styles['Normal']))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
