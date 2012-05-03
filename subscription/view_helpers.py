import cStringIO
import os

from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from django.conf import settings as s

from core.templatetags.filters import format_unix_time


def get_or_create_receipt_pdf(charge, employer_name):
    pdf_name = "Umeqo_Charge_%s_%s.pdf" % (format_unix_time(charge.created).replace("/", "-"), charge.id)
    path = "%semployer/receipts/" % (s.MEDIA_ROOT)
    pdf_path = "%s%s" % (path, pdf_name)
    if not os.path.exists(pdf_path):
        output = PdfFileWriter()
        
        report_buffer = cStringIO.StringIO() 
        c = Canvas(report_buffer)  
        #first_line = "Created on %s at %s" % (now.strftime('%m/%d/%Y'), now.strftime('%I:%M %p'))
        c.drawString(1*cm, 28*cm, employer_name)
        c.drawString(1*cm, 29*cm, charge.id)
        c.showPage()
        c.save()
        cString = cStringIO.StringIO(report_buffer.getvalue())
        
        output.addPage(PdfFileReader(cString).getPage(0))
        if not os.path.exists(path):
            os.makedirs(path)
        outputStream = file(pdf_path, "wb")
        output.write(outputStream)
        outputStream.close()
    return pdf_path