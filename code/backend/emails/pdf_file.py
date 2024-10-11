import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def pdf_file(content):
    pdf_filename = 'result_' + format(time.time(), '.0f') + '.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, content)
    c.showPage()
    c.save()
    return pdf_filename
