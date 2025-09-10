from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from pathlib import Path
from PIL import Image as PILImage
import io

def _load_logo_scaled(max_width_pts: float):
    candidates = [
        Path("assets/logo.png"),
        Path("assets/Logo.png"),
        Path("assets/logo.jpg"),
        Path("assets/Logo.jpg"),
    ]
    path = next((p for p in candidates if p.exists()), None)
    if not path:
        return None

    try:
        with PILImage.open(path) as im:
            w_px, h_px = im.size
            dpi = im.info.get("dpi", (72, 72))[0] or 72

        w_pt = (w_px / dpi) * 72
        h_pt = (h_px / dpi) * 72

        scale = 1.0
        if w_pt > max_width_pts:
            scale = max_width_pts / w_pt

        draw_w = w_pt * scale
        draw_h = h_pt * scale

        img = Image(str(path))
        img.drawWidth = draw_w
        img.drawHeight = draw_h
        img.hAlign = "CENTER"
        return img
    except Exception:
        return None

def create_report(result: dict, impressum_url: str, datenschutz_url: str, contact_email: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    h2 = styles["Heading2"]
    story = []

    logo_flow = _load_logo_scaled(doc.width)
    if logo_flow:
        story.append(logo_flow)
        story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("EU AI Act Quick-Check", styles["Title"]))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph(f"<b>Ergebnis:</b> {result['risk']}", normal))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("<b>Begründungen:</b>", h2))
    if result.get("reasons"):
        for r in result["reasons"]:
            story.append(Paragraph(f"• {r}", normal))
    else:
        story.append(Paragraph("Keine besonderen Risiken.", normal))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("<b>Nächste Schritte:</b>", h2))
    for t in result.get("tasks", []):
        story.append(Paragraph(f"• {t}", normal))

    story.append(Spacer(1, 10 * mm))

    link_color = colors.HexColor("#2563EB")
    story.append(Paragraph(
        f"""<font size=9>
        © 2025 KN-AI-Solutions ·
        <link href="{impressum_url}" color="{link_color}">Impressum</link> ·
        <link href="{datenschutz_url}" color="{link_color}">Datenschutz</link> ·
        Kontakt: <link href="mailto:{contact_email}" color="{link_color}">{contact_email}</link>
        </font>""",
        normal
    ))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
