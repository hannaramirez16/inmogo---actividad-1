from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime

class PDFGenerator:
    
    @staticmethod
    def generar_contrato(contrato):
        """Genera un PDF del contrato de arrendamiento"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        story.append(Paragraph("CONTRATO DE ARRENDAMIENTO", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Información del contrato
        content = f"""
        <b>Número de Contrato:</b> {contrato.numero_contrato}<br/>
        <b>Fecha de Emisión:</b> {datetime.now().strftime('%d/%m/%Y')}<br/><br/>
        
        <b>PROPIETARIO</b><br/>
        Nombre: {contrato.propietario.get_full_name()}<br/>
        Documento: {contrato.propietario.documento_identidad}<br/>
        Email: {contrato.propietario.email}<br/>
        Teléfono: {contrato.propietario.telefono}<br/><br/>
        
        <b>INQUILINO</b><br/>
        Nombre: {contrato.inquilino.get_full_name()}<br/>
        Documento: {contrato.inquilino.documento_identidad}<br/>
        Email: {contrato.inquilino.email}<br/>
        Teléfono: {contrato.inquilino.telefono}<br/><br/>
        
        <b>INMUEBLE</b><br/>
        {contrato.inmueble.titulo}<br/>
        Dirección: {contrato.inmueble.direccion}<br/>
        Ciudad: {contrato.inmueble.ciudad}<br/><br/>
        
        <b>CONDICIONES ECONÓMICAS</b><br/>
        """
        
        story.append(Paragraph(content, styles['BodyText']))
        
        # Tabla de valores
        data = [
            ['Concepto', 'Valor'],
            ['Valor Arriendo Mensual', f'${contrato.valor_arriendo:,.0f}'],
            ['Valor Administración', f'${contrato.valor_administracion:,.0f}'],
            ['Depósito en Garantía', f'${contrato.deposito_garantia:,.0f}'],
            ['Día de Pago', str(contrato.dia_pago)],
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Spacer(1, 0.2*inch))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Fechas del contrato
        fechas = f"""
        <b>VIGENCIA DEL CONTRATO</b><br/>
        Fecha de Inicio: {contrato.fecha_inicio.strftime('%d/%m/%Y')}<br/>
        Fecha de Finalización: {contrato.fecha_fin.strftime('%d/%m/%Y')}<br/>
        Duración: {contrato.duracion_meses} meses<br/><br/>
        """
        
        story.append(Paragraph(fechas, styles['BodyText']))
        
        if contrato.clausulas_especiales:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("<b>CLÁUSULAS ESPECIALES</b>", styles['Heading2']))
            story.append(Paragraph(contrato.clausulas_especiales, styles['BodyText']))
        
        # Firmas
        story.append(Spacer(1, inch))
        firmas = """
        <br/><br/>
        ___________________________ ___________________________<br/>
        Firma Propietario &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Firma Inquilino<br/>
        """
        story.append(Paragraph(firmas, styles['BodyText']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_cuenta_cobro(cuenta):
        """Genera un PDF de la cuenta de cobro"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#d32f2f'),
            spaceAfter=30,
            alignment=1
        )
        
        story.append(Paragraph("CUENTA DE COBRO", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Información
        content = f"""
        <b>Número de Cuenta:</b> {cuenta.numero_cuenta}<br/>
        <b>Fecha de Emisión:</b> {cuenta.fecha_emision.strftime('%d/%m/%Y')}<br/>
        <b>Fecha de Vencimiento:</b> {cuenta.fecha_vencimiento.strftime('%d/%m/%Y')}<br/><br/>
        
        <b>INQUILINO</b><br/>
        Nombre: {cuenta.inquilino.get_full_name()}<br/>
        Documento: {cuenta.inquilino.documento_identidad}<br/>
        Email: {cuenta.inquilino.email}<br/><br/>
        
        <b>CONCEPTO:</b> {cuenta.get_concepto_display()}<br/>
        <b>PERÍODO:</b> {cuenta.periodo_inicio.strftime('%d/%m/%Y')} - {cuenta.periodo_fin.strftime('%d/%m/%Y')}<br/><br/>
        """
        
        if cuenta.descripcion:
            content += f"<b>DESCRIPCIÓN:</b><br/>{cuenta.descripcion}<br/><br/>"
        
        story.append(Paragraph(content, styles['BodyText']))
        
        # Tabla de valores
        data = [
            ['Concepto', 'Valor'],
            ['Valor Total', f'${cuenta.valor_total:,.0f}'],
            ['Valor Pagado', f'${cuenta.valor_pagado:,.0f}'],
            ['Valor Mora', f'${cuenta.valor_mora:,.0f}'],
            ['<b>Valor Pendiente</b>', f'<b>${cuenta.valor_pendiente:,.0f}</b>'],
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*inch))
        
        # Información de pago
        info_pago = """
        <b>INFORMACIÓN DE PAGO</b><br/>
        Por favor realizar el pago antes de la fecha de vencimiento.<br/>
        Para más información contactar a la administración.<br/>
        """
        story.append(Paragraph(info_pago, styles['BodyText']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer