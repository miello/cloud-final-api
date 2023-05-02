from PyPDF3 import PdfFileMerger, PdfFileWriter, PdfFileReader
import random
import os
import io

merger = PdfFileMerger()
file_dir = os.path.dirname(os.path.realpath('__file__'))
base_path = os.path.join(file_dir, "assets/watermark/")
watermark = ["watermark1.pdf","watermark2.pdf"]
merged_file = "merged.pdf"

def jerm_resume(pdf_file):
    input_pdf = PdfFileReader(pdf_file)
    watermark_pdf = PdfFileReader(open(base_path+random.choice(watermark), "rb"))

    pdf_page = input_pdf.getPage(0)
    pdf_page.mergePage(watermark_pdf.getPage(0))

    output = PdfFileWriter()
    output.addPage(pdf_page)

    return io.BytesIO(output)
