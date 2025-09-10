from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

def create_report(result, logo_path="assets/Logo.png"):
    from io import BytesIO
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Logo groß einfügen (halbe Seitenbreite)
    try:
        logo = Image(logo_path, width=250, height=100)  # skaliert ohne Verzerrung
        story.append(logo)
        story.append(Spacer(1, 20))
    except Exception as e:
        story.append(Paragraph("Logo konnte nicht geladen werden.", styles['Normal']))

    story.append(Paragraph("<b>EU AI Act Quick-Check</b>", styles['Title']))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Ergebnis:</b> {result['risk']}", styles['Normal']))
    reasons = "; ".join(result["reasons"]) or "Kontrollen wirken ausreichend."
    story.append(Paragraph(f"<b>Begründung:</b> {reasons}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Nächste Schritte:</b>", styles['Normal']))
    for t in result["tasks"]:
        story.append(Paragraph(f"• {t}", styles['Normal']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
