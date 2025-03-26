import time
from docx import Document


def docx_file(content):
    docx_filename = 'result_' + format(time.time(), '.0f') + '.docx'
    doc = Document()
    doc.add_paragraph(content)
    doc.save(docx_filename)
    return docx_filename
