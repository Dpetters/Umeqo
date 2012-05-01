import cStringIO

from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

def create_charge_page(charge, employer):
    report_buffer = cStringIO.StringIO() 
    c = Canvas(report_buffer)  
    #first_line = "Created on %s at %s" % (now.strftime('%m/%d/%Y'), now.strftime('%I:%M %p'))
    c.drawString(1*cm, 28*cm, str(employer))
    c.drawString(1*cm, 29*cm, charge.id)
    c.showPage()
    c.save()
    return cStringIO.StringIO(report_buffer.getvalue())