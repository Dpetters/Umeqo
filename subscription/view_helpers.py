import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer

from django.conf import settings as s

from core.templatetags.filters import format_money, format_unix_time

width, height = A4
styles = getSampleStyleSheet()

right_align_style = ParagraphStyle(name='BodyText', parent=styles['Normal'], alignment=TA_RIGHT)

def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

def get_or_create_receipt_pdf(charge, invoice, employer_name):
    pdf_name = "Umeqo_Charge_%s_%s.pdf" % (format_unix_time(charge.created).replace("/", "-"), charge.id)
    path = "%semployer/receipts/" % (s.MEDIA_ROOT)
    if not os.path.exists(path):
        os.makedirs(path)
    pdf_path = "%s%s" % (path, pdf_name)
    if not os.path.exists(pdf_path):
        story = []
        story.append(Spacer(3*cm, 2*cm))
        
        story.append(Paragraph('Umeqo Receipt', styles['Heading1']))
        story.append(Paragraph(employer_name, styles['Heading2']))
        story.append(Paragraph("Charge ID: %s" % charge.id, styles['Heading3']))
        story.append(Spacer(1*cm, 1*cm))

        hitem = Paragraph('''<b>Item</b>''', styles["Normal"])
        hdate = Paragraph('''<b>Date</b>''', styles["Normal"])
        hamount = Paragraph('''<b>Amount</b>''', styles["Normal"])

        data= [[hitem, hdate,  hamount]]
                
        for subscription in invoice.lines.subscriptions:
            item = Paragraph(subscription.plan.name, styles["Normal"])
            date = Paragraph("%s-%s" % (format_unix_time(subscription.period.start), format_unix_time(subscription.period.end)), styles["Normal"])
            amount = Paragraph("$" + format_money(subscription.amount), right_align_style)
            data.append([item, date, amount])

        for invoice_item in invoice.lines.invoiceitems:
            item = Paragraph(invoice_item.description, styles["Normal"])
            date = Paragraph(format_unix_time(invoice_item.date), styles["Normal"])
            amount = Paragraph("$" + format_money(invoice_item.amount), right_align_style)
            data.append([item, date, amount])

        for proration in invoice.lines.prorations:
            item = Paragraph(proration.description, styles["Normal"])
            date = Paragraph(format_unix_time(proration.date), styles["Normal"])
            amount = Paragraph("$" + format_money(proration.amount), right_align_style)
            data.append([item, date, amount])
        
        
        table = Table(data, colWidths=[8.5 * cm, 4.5 * cm, 2.5 * cm])
        
        table.setStyle(TableStyle([
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ]))
        
        story.append(table)
        
        total_amount_style = ParagraphStyle(name='BodyText', parent=styles['Normal'], alignment=TA_RIGHT, spaceBefore=1)
        total_amount = Paragraph("<strong>Total:</strong> $%s" % format_money(charge.amount), total_amount_style)
        story.append(total_amount)
        
        
        story.append(Spacer(1*cm, 3*cm))

        story.append(Paragraph('''Umeqo''', styles["Normal"]))
        story.append(Paragraph('''305 Memorial Drive #5037''', styles["Normal"]))
        story.append(Paragraph('''Cambridge, MA 02139''', styles["Normal"]))
        story.append(Paragraph('''''', styles["Normal"]))
        story.append(Paragraph('''Web: http://umeqo.com''', styles["Normal"]))
        story.append(Paragraph('''Phone: (425) 681-2953''', styles["Normal"]))        
        
        doc = SimpleDocTemplate(pdf_path, pagesize = A4, topMargin=0)
        doc.build(story)
    return pdf_path