# logic/report.py — PDF ohne Verzerrung, mit großem Logo

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from PIL import Image as PILImage
import io

def _find_logo_path():
    for p in [Path("assets/Logo.png"), Path("assets/logo.png")]:
        if p.exists():
            return p
    return None

def _image_flowable_proportional(path: Path, target_width_cm: float):
    """Erzeugt ein reportlab-Image mit beibehaltener Proportion, nur Breite vorgegeben."""
    try:
        with PILImage.open(path) as im:
            w, h = im.size
            if not w or not h:
                return None
            target_w = target_width_cm * cm
            target_h = target_w * (h / w)
        return Image(str(path), width=target_w, height=target_h)
    except Exception:
        return None

def create_report(result: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    elements = []

    # Logo groß, proportional (z. B. ~12 cm breit)
    logo_path = _find_logo_path()
    if logo_path:
        logo_img = _image_flowable_proportional(logo_path, target_width_cm=12.0)
        if logo_img:
            elements.append(logo_img)
            elements.append(Spacer(1, 0.8*cm))

    # Titel
    elements.append(Paragraph("EU AI Act Quick-Check – Ergebnisbericht", styles['Title']))
    elements.append(Spacer(1, 0.6*cm))

    # Ergebnis
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
