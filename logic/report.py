from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from pathlib import Path
from PIL import Image as PILImage
import io


def _load_logo_scaled(max_width_pts: float):
    """
    Lädt das Logo, skaliert es proportional auf max_width_pts (Punkte) herunter
    und gibt ein reportlab Image-Flowable zurück (oder None).
    """
    # Kandidaten (Groß-/Kleinschreibung)
    candidates = [
        Path("assets/logo.png"),
        Path("assets/Logo.png"),
        Path("assets/logo.jpg"),
        Path("assets/Logo.jpg"),
        Path("assets/logo.jpeg"),
        Path("assets/Logo.jpeg"),
    ]
    path = next((p for p in candidates if p.exists()), None)
    if not path:
        return None

    try:
        # Originalgröße in Pixel lesen
        with PILImage.open(path) as im:
            w_px, h_px = im.size

        # ReportLab benutzt Punkte (1 pt ≈ 1/72 Zoll)
        # Wir wollen das Bild *proportional* bis max_width_pts skalieren
        # und dabei die Höhe passend mitskalieren (kein "Quetschen").
        # Grundlage: DPI – wenn nicht gesetzt, nehmen wir 72 dpi als Fallback.
        dpi = 72
        # Manche Bilder haben DPI in info
        if "dpi" in im.info and isinstance(im.info["dpi"], tuple):
            try:
                dpi = im.info["dpi"][0] or 72
            except Exception:
                dpi = 72

        # Pixel -> Punkte umrechnen
        w_pt = (w_px / dpi) * 72
        h_pt = (h_px / dpi) * 72

        # Falls zu breit: proportional verkleinern
        scale = 1.0
        if w_pt > max_width_pts:
            scale = max_width_pts / w_pt

        draw_w = w_pt * scale
        draw_h = h_pt * scale

        img = Image(str(path))
        img.drawWidth = draw_w
        img.drawHeight = draw_h
        img.hAlign = "CENTER"  # zentriert
        return img
    except Exception:
        return None


def create_report(result: dict) -> bytes:
    """
    Erstellt einen PDF-Report mit Logo (proportional skaliert) und Assessment-Ergebnis.
    Gibt ein Byte-Objekt zurück, das Streamlit direkt zum Download anbieten kann.
    """
    buffer = io.BytesIO()

    # Dokument mit angenehmen Rändern
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    # ----- Logo (breit & proportional) -----
    # verfügbare Breite des Inhaltsbereichs
    available_width = doc.width  # A4 minus Ränder
    logo_flowable = _load_logo_scaled(available_width)
    if logo_flowable:
        story.append(logo_flowable)
        story.append(Spacer(1, 8 * mm))

    # ----- Titel -----
    story.append(Paragraph("EU AI Act Quick-Check", styles["Title"]))
    story.append(Spacer(1, 4 * mm))

    # ----- Ergebnis -----
    story.append(Paragraph(f"<b>Ergebnis:</b> {result['risk']}", styles["Normal"]))
    story.append(Spacer(1, 4 * mm))

    # ----- Begründungen -----
    story.append(Paragraph("<b>Begründungen:</b>", styles["Heading2"]))
    if result.get("reasons"):
        for r in result["reasons"]:
            story.append(Paragraph(f"• {r}", styles["Normal"]))
    else:
        story.append(Paragraph("Keine besonderen Risiken.", styles["Normal"]))
    story.append(Spacer(1, 4 * mm))

    # ----- Nächste Schritte -----
    story.append(Paragraph("<b>Nächste Schritte:</b>", styles["Heading2"]))
    for t in result.get("tasks", []):
        story.append(Paragraph(f"• {t}", styles["Normal"]))

    # PDF erzeugen
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
