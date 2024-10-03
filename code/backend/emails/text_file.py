import time


def text_file(content):
    txt_filename = 'result_' + format(time.time(), '.0f')

    with open(txt_filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(content)

    return txt_filename
