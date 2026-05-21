from reportlab.lib.pagesizes import letter

from reportlab.pdfgen import canvas

def generate_pdf_report(

    transaction_reference,
    fraud_type,
    risk_level,
    analyst_notes
):

    file_name = (
        f"{transaction_reference}_report.pdf"
    )

    c = canvas.Canvas(
        file_name,
        pagesize=letter
    )

    c.setFont(
        "Helvetica-Bold",
        20
    )

    c.drawString(
        100,
        750,
        "MT500 Fraud Investigation Report"
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawString(
        100,
        700,
        f"Transaction Reference: "
        f"{transaction_reference}"
    )

    c.drawString(
        100,
        670,
        f"Fraud Type: "
        f"{fraud_type}"
    )

    c.drawString(
        100,
        640,
        f"Risk Level: "
        f"{risk_level}"
    )

    c.drawString(
        100,
        610,
        "Analyst Notes:"
    )

    c.drawString(
        120,
        580,
        analyst_notes
    )

    c.save()

    return file_name