from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(content, filepath):
    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()
    elements = []

    for line in content.split("\n"):
        if line.strip():
            elements.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )
            elements.append(
                Spacer(1, 5)
            )
    doc.build(elements)
    return filepath