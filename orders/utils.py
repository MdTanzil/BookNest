from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import black
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus import HRFlowable, Table, TableStyle
from reportlab.lib.colors import black, white, HexColor

def generate_shipping_label(response, order):
    """
    Generates a localized international courier shipping label PDF stream safely.
    """
    LABEL_WIDTH = 4 * inch
    LABEL_HEIGHT = 6 * inch
    
    doc = SimpleDocTemplate(
        response,
        pagesize=(LABEL_WIDTH, LABEL_HEIGHT),
        leftMargin=0.2*inch, rightMargin=0.2*inch,
        topMargin=0.2*inch, bottomMargin=0.2*inch
    )

    story = []
    styles = getSampleStyleSheet()
    
    header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=9, leading=11, fontName="Helvetica-Bold")
    text_style = ParagraphStyle('Text', parent=styles['Normal'], fontSize=10, leading=13, fontName="Helvetica")
    address_style = ParagraphStyle('Address', parent=styles['Normal'], fontSize=11, leading=14, fontName="Helvetica-Bold")
    cod_style = ParagraphStyle('COD', parent=styles['Normal'], fontSize=15, leading=17, fontName="Helvetica-Bold", textColor=black)
    zone_style = ParagraphStyle('Zone', parent=styles['Normal'], fontSize=13, leading=15, fontName="Helvetica-Bold")

    # 1. Merchant Identity Branding Header
    story.append(Paragraph("MERCHANT: BOOKNEST BD", header_style))
    story.append(Paragraph("Bkash/Nagad Wallet: 017XXXXXXXX", text_style))
    story.append(Spacer(1, 0.05 * inch))
    
    # Divider vector line rule
    d_line = Drawing(3.6 * inch, 2)
    d_line.add(Rect(0, 0, 3.6 * inch, 2, fillColor=black, strokeColor=black))
    story.append(d_line)
    story.append(Spacer(1, 0.1 * inch))

    # 2. Localized Geographical Sorting Coordinates
    story.append(Paragraph(f"DESTINATION HUB: {order.shipping_city.upper()}", zone_style))
    story.append(Paragraph(f"THANA/POSTCODE: {order.shipping_postcode}", text_style))
    story.append(Spacer(1, 0.08 * inch))
    story.append(d_line)
    story.append(Spacer(1, 0.1 * inch))

    # 3. Recipient Info
    story.append(Paragraph("SHIP TO:", header_style))
    story.append(Paragraph(order.shipping_name, address_style))
    story.append(Paragraph(order.shipping_address, text_style))
    story.append(Paragraph(f"CUSTOMER PHONE: {order.shipping_phone}", address_style))
    story.append(Spacer(1, 0.08 * inch))
    story.append(d_line)
    story.append(Spacer(1, 0.1 * inch))

    # 4. Cash On Delivery Matrix Parameter Blocks
    if order.payment_method == 'Cash on Delivery':
        cod_text = f"CASH TO COLLECT: BDT {order.total}"
    else:
        cod_text = "PAID - COLLECT BDT 0"
        
    story.append(Paragraph(cod_text, cod_style))
    story.append(Paragraph(f"Payment Class: {order.payment_method}", text_style))
    story.append(Paragraph(f"Order Reference: #{order.order_number}", text_style))
    story.append(Spacer(1, 0.15 * inch))

    # 5. Delivery Hub Tracking Barcode Engine (FIXED: Append natively to story)
    # Renders the barcode as a standalone flowable block, with human-readable tracking text below
    barcode = code128.Code128(order.order_number, barHeight=0.45*inch, barWidth=1.2, humanReadable=True)
    story.append(barcode)

    doc.build(story)




def generate_customer_receipt(response, order, items):
    """
    Generates a professional corporate A4 customer purchase receipt PDF stream.
    """
    # Initialize standard A4 document layout matrix configurations
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch
    )

    story = []
    styles = getSampleStyleSheet()
    
    # Custom typographical rules
    title_style = ParagraphStyle('RecTitle', parent=styles['Heading1'], fontSize=24, leading=28, fontName="Helvetica-Bold", textColor=HexColor("#264b5d"))
    meta_bold = ParagraphStyle('MetaB', parent=styles['Normal'], fontSize=10, leading=14, fontName="Helvetica-Bold")
    meta_text = ParagraphStyle('MetaT', parent=styles['Normal'], fontSize=10, leading=14, fontName="Helvetica")
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontSize=10, leading=12, fontName="Helvetica-Bold", textColor=white)
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontSize=10, leading=13, fontName="Helvetica")

    # 1. Header Grid Row (Brand Info vs Invoice Metadata)
    header_data = [
        [Paragraph("BOOKNEST BD", title_style), Paragraph(f"<b>INVOICE:</b> #{order.order_number}", meta_text)],
        [Paragraph("Dhaka, Bangladesh<br/>Email: support@booknest.com", meta_text), Paragraph(f"<b>Date:</b> {order.created_at.strftime('%d %b, %Y')}<br/><b>Status:</b> {order.status}", meta_text)]
    ]
    header_table = Table(header_data, colWidths=[4.0*inch, 3.25*inch])
    header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(header_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#264b5d"), spaceAfter=15))

    # 2. Billing & Shipping Metadata Column Blocks
    info_data = [
        [Paragraph("<b>Customer Details:</b>", meta_bold), Paragraph("<b>Shipping Address:</b>", meta_bold)],
        [Paragraph(f"{order.shipping_name}<br/>Phone: {order.shipping_phone}", meta_text), Paragraph(f"{order.shipping_address}<br/>{order.shipping_city} - {order.shipping_postcode}", meta_text)]
    ]
    info_table = Table(info_data, colWidths=[3.6*inch, 3.6*inch])
    info_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(info_table)
    
    story.append(Spacer(1, 0.3*inch))

    # 3. Itemized Purchased Books Table Matrix
    table_data = [[Paragraph("Book Title", th_style), Paragraph("Price", th_style), Paragraph("Qty", th_style), Paragraph("Total", th_style)]]
    
    # Loop over database pre-fetched order items lines
    for item in items:
        title = item.book.title if item.book else "Removed Book Title"
        table_data.append([
            Paragraph(title, td_style),
            Paragraph(f"BDT {item.price}", td_style),
            Paragraph(str(item.quantity), td_style),
            Paragraph(f"BDT {item.total}", td_style)
        ])
        
    # Append Financial Accounting Summary Totals Rows
    table_data.append(["", "", Paragraph("<b>Subtotal:</b>", meta_text), Paragraph(f"BDT {order.subtotal}", meta_text)])
    table_data.append(["", "", Paragraph("<b>Shipping Cost:</b>", meta_text), Paragraph(f"BDT {order.shipping_cost}", meta_text)])
    if order.discount > 0:
        table_data.append(["", "", Paragraph("<b>Discount:</b>", meta_text), Paragraph(f"- BDT {order.discount}", meta_text)])
    table_data.append(["", "", Paragraph("<b>Grand Total:</b>", meta_bold), Paragraph(f"<b>BDT {order.total}</b>", meta_bold)])

    # Dynamically find the index row where the items end and totals begin
    divider_row_idx = len(items) + 1

    item_table = Table(table_data, colWidths=[4.2*inch, 1.1*inch, 0.7*inch, 1.2*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#264b5d")),
        ('ALIGN', (1,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('ROWBACKGROUNDS', (0,1), (-1, len(items)), [white, HexColor("#f9f9f9")]),
        ('GRID', (0,0), (-1, len(items)), 0.5, HexColor("#e0e0e0")),
        
        # FIXED: Removed nested tuple components. Using clean flat array ranges instead.
        ('LINEABOVE', (2, divider_row_idx), (3, -1), 1, HexColor("#264b5d")),
        ('TOPPADDING', (2, divider_row_idx), (3, -1), 6),
    ]))
    
    story.append(item_table)
    story.append(Spacer(1, 0.4*inch))
    
    # 4. Institutional Terms & Footer Notice Blocks
    story.append(Paragraph("<b>Terms & Conditions:</b>", meta_bold))
    story.append(Paragraph("1. Please preserve this purchase receipt copy to process any localized book return or verification requests within 7 days.", td_style))
    story.append(Paragraph(f"2. Method of Payment processed successfully via: <b>{order.payment_method}</b>.", td_style))
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("<center>Thank you for buying from BookNest BD! Reading feeds the soul.</center>", meta_bold))

    doc.build(story)
