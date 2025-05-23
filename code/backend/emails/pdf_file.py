import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def pdf_file(content):
    pdf_filename = 'result_' + format(time.time(), '.0f') + '.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    y = height - 40
    max_width = width - 80

    if not isinstance(content, str):
        content = str(content)

    lines = content.split("\n")
    for line in lines:
        wrapped_lines = simpleSplit(line, "Helvetica", 12, max_width)
        for wline in wrapped_lines:
            if y < 40:
                c.showPage()
                y = height - 40
            c.drawString(40, y, wline)
            y -= 20

    c.save()
    return pdf_filename