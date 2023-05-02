from PyPDF3 import PdfFileMerger, PdfFileWriter, PdfFileReader
import random

merger = PdfFileMerger()

base_path = "./assets/watermark"
pdf_file = "doc.pdf"
watermark = ["watermark1.pdf","watermark2.pdf"]
merged_file = "merged.pdf"

def jerm(pdf_file):
    input_pdf = PdfFileReader(pdf_file)
    watermark_pdf = PdfFileReader(open(base_path+random.choice(watermark), "rb"))

    pdf_page = input_pdf.getPage(0)
    pdf_page.mergePage(watermark_pdf.getPage(0))

    output = PdfFileWriter()
    output.addPage(pdf_page)

    return open(merged_file,'wb')
