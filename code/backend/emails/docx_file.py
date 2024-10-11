import time
from docx import Document


def docx_file(content):
    docx_filename = 'result_' + format(time.time(), '.0f') + '.docx'
    doc = Document()
    doc.add_paragraph(content)  # 添加段落
    doc.save(docx_filename)
    return docx_filename
