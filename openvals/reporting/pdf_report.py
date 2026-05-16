from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    recommendation,
    output_path
):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "OpenVals AI Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Recommended Model: "
            f"{recommendation['recommended_model']}",
            styles["BodyText"]
        )
    )

    doc.build(elements)