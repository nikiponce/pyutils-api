from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import datetime
import locale
import io

FONT_PATH = "/app/assets/fonts/Inter.ttf"
# FONT_PATH = "/app/assets/fonts/Sigmar.ttf"
pdfmetrics.registerFont(TTFont("Inter", "/app/assets/fonts/Inter.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "/app/assets/fonts/Inter-Bold.ttf"))

def generate_pdf_from_json_data(json_data):
    
    data = json_data

    # Verificar si data es una lista
    if not isinstance(data, list):
        raise ValueError("El JSON debe contener una lista de expedientes.")
    # Establecer el locale en español
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES')  # Intenta con español de España
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'es')  # Intenta con español genérico
        except locale.Error:
            print("Advertencia: No se pudo establecer el locale en español.")

    buffer = io.BytesIO()  # Usar un buffer en memoria en lugar de un archivo físico
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.1*inch, bottomMargin=0.5*inch, leftMargin=0.4*inch, rightMargin=0.4*inch)
    styles = getSampleStyleSheet()

    story = []  # Lista para almacenar los elementos del PDF

    # Estilos personalizados (usando fuentes estándar)
    title_style = ParagraphStyle(
        name='TitleStyle', # Nombre del estilo
        fontName='Inter-Bold', # Fuente en negrita
        fontSize=12, # Tamaño de la fuente     
        textColor=HexColor("#D50057"), # Color de texto
        alignment=0,  # Alineado a la izquierda
        leading=14, # Espacio entre líneas  
        spaceBefore=6,  # Reduce space antes del titulo
        spaceAfter=6,   # Reduce space despues del titulo
        borderPadding=0 # Reduce padding del borde        
    )

    info_style = ParagraphStyle(
        name='InfoStyle', # Nombre del estilo   
        fontName='Inter', # Fuente normal
        fontSize=8, # Tamaño de la fuente
        alignment=0,  # Alineado a la izquierda
    )

    section_title_style = ParagraphStyle(
        name='SectionTitleStyle', # Nombre del estilo
        fontName='Inter-Bold', # Fuente en negrita
        textColor=HexColor("#262626"), # Color de texto
        fontSize=10, # Tamaño de la fuente
        alignment=0,  # Alineado a la izquierda
    )

    summary_style = ParagraphStyle(
        name='SummaryStyle', # Nombre del estilo
        fontName='Inter', # Fuente normal
        fontSize=10, # Tamaño de la fuente
        alignment=0, # Alineado a la izquierda
    )

    normal_style = ParagraphStyle(
        name='NormalStyle', # Nombre del estilo
        fontName='Inter', # Fuente normal
        fontSize=8, # Tamaño de la fuente
        alignment=0, # Alineado a la izquierda
        leading=12, # Espacio entre líneas
    )

    normal_style_centered = ParagraphStyle(
        name='NormalStyleCentered', # Nombre del estilo
        fontName='Inter-Bold', # Fuente normal
        fontSize=8, # Tamaño de la fuente 
        alignment=1, # Alineado al centro
        leading=12, # Espacio entre líneas
        )
   
    
    # Iterar a través de cada expediente en la lista
    for expediente_data in data:
        
        # Obtener la fecha actual
        fecha_hoy = datetime.date.today()
        dia = fecha_hoy.day
        mes = fecha_hoy.strftime("%B")  # Nombre completo del mes
        anio = fecha_hoy.year

        # Formatear la fecha en el formato deseado
        fecha_formateada = f"Dia <b>{dia}</b> de <b>{mes}</b> de <b>{anio}</b>"
        fecha_hoy_text = Paragraph(fecha_formateada, info_style)

        # Crear una tabla para alinear la fecha actual a la derecha
        data_fecha_hoy = [["", fecha_hoy_text]]
        table_fecha_hoy = Table(data_fecha_hoy, colWidths=[6.5*inch, 1.5*inch])
        table_fecha_hoy.setStyle(TableStyle([
            ('ALIGN', (0, 0), (1, 0), 'LEFT'), # Alinear a la izquierda
            ('FONTNAME', (0, 0), (-1, -1), 'Inter'), # Fuente
            ('FONTSIZE', (0, 0), (-1, -1), 8), # Tamaño de la fuente
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black), # Color del texto
            ('LEFTPADDING', (0, 0), (-1, -1), 0), # Padding izquierdo
            ('RIGHTPADDING', (0, 0), (-1, -1), 0), # Padding derecho
            ('TOPPADDING', (0, 0), (-1, -1), 0), # Padding superior
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0), # Padding inferior
        ]))
        story.append(table_fecha_hoy)

        # Obtener el nombre del expediente del JSON
        nombre_expediente = expediente_data.get("expedientName", "Informe Legal")
        
        # Título principal
        title = Paragraph(nombre_expediente, title_style)
        story.append(title)

        # Separador
        story.append(Spacer(1, 0.2*inch)) # Espacio después del título
        story.append(HRFlowable(width="100%", color=colors.black, thickness=1)) # Línea horizontal
        story.append(Spacer(1, 0.2*inch))  # Espacio después del separador

        # Crear una tabla para alinear la información
        data_info = [[[Paragraph("<b>Modificado por:</b> " +  expediente_data.get("modifiedBy", ""), normal_style)],Paragraph("<b>Última actualización:</b> " + expediente_data.get("modifiedDate", ""), normal_style), Paragraph("<b>Situación:</b> " + expediente_data.get("situation", "") , normal_style)]]

        # Definir el ancho de la tabla principal
        table_width = 7.5 * inch  # Ancho total de la tabla (8.5 - 1 pulgada de margen a cada lado)
        col_widths_info = [table_width * 0.5, table_width * 0.3, table_width * 0.2]

        table_info = Table(data_info, colWidths=col_widths_info)
        table_info.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Inter'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(table_info)

        #########################################
        #        Resumen del expediente         #
        #########################################
       
        story.append(Spacer(1, 0.1*inch))
        resumen_title = Paragraph("Resumen del expediente", section_title_style)
        story.append(resumen_title)

        story.append(Spacer(1, 0.1*inch))

          # Datos del expediente en un cuadro sombreado
        data_resumen = [
            [Paragraph("<b>Titular:</b> " +  expediente_data.get("titular", ""), normal_style)],
            [Paragraph("<b>Responsable:</b> " + expediente_data.get("responsable", ""), normal_style)],
            [Paragraph("<b>Cliente:</b> " + expediente_data.get("cliente", "") + "  -  " + "<b>Contrario:</b> " + expediente_data.get("contrario", ""), normal_style)],
            [Paragraph("<b>Órgano:</b> " + expediente_data.get("organo", "") +  "  -  " +  "<b>Nº Autos:</b> " + expediente_data.get("numAutos", ""), normal_style)]
        ]

        # col_widths_resumen = [table_width * 0.25, table_width * 0.25, table_width * 0.25, table_width * 0.25]
        col_widths_resumen = [table_width]

        table_resumen = Table(data_resumen, colWidths=col_widths_resumen)
        table_resumen.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor("#F7F7F7")),
            ('FONTNAME', (0, 0), (-1, -1), 'Inter'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(table_resumen)

        #########################################
        #        Tabla de Intervinientes        #
        #########################################

        if expediente_data.get("intervinientes"):
            story.append(Spacer(1, 0.1*inch))
            intervinientes_title = Paragraph("Intervinientes", section_title_style)
            story.append(intervinientes_title)
            story.append(Spacer(1, 0.1*inch))

            intervinientes_data = [["Tipo", "Nombre", "Nº Identificación", "Teléfono"]]
            for intervinientes in expediente_data.get("intervinientes", []):
                intervinientes_data.append([
                    Paragraph(str(intervinientes.get("tipo", "")), normal_style),
                    Paragraph(intervinientes.get("nombre", ""), normal_style),
                    Paragraph(intervinientes.get("identificacion", ""), normal_style),                
                    Paragraph(intervinientes.get("telefono", ""), normal_style),                
                ])

            col_widths_intervinientes = [table_width * 0.2, table_width * 0.3998, table_width * 0.2, table_width * 0.2]

            intervinientes_table = Table(intervinientes_data, colWidths=col_widths_intervinientes)
            intervinientes_table.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#001978")),  # Blue header text
                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Inter'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),         
                ('BOTTOMPADDING', (0, 0), (-1, 0), 2),        
                ('TOPPADDING', (0, 0), (-1, 0), 2),       
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),        
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor("#001978")),        
                ('LINEBELOW', (0, 1), (-1, -1), 0.5, HexColor("#DDDCDC")),
            ]))
            story.append(intervinientes_table)

        #########################################
        #        Tabla de Datos economicos      #
        #########################################

        if expediente_data.get("datosEconomicos"):
            story.append(Spacer(1, 0.1*inch))
            datos_economicos_title = Paragraph("Datos económicos", section_title_style)
            story.append(datos_economicos_title)
            story.append(Spacer(1, 0.1*inch))

            datos_economicos_data = [["Tipo", "Fecha", "Descripcón", "Importe"]]
            for datos_economicos in expediente_data.get("datosEconomicos", []):
                datos_economicos_data.append([
                    Paragraph(str(datos_economicos.get("tipo", "")), normal_style),
                    Paragraph(datos_economicos.get("fecha", ""), normal_style),
                    Paragraph(datos_economicos.get("descripcion", ""), normal_style),                
                    Paragraph(datos_economicos.get("importe", ""), normal_style),                
                ])

            col_widths_datos_economicos = [table_width * 0.2, table_width * 0.2, table_width * 0.3998, table_width * 0.2]

            datos_economicos_table = Table(datos_economicos_data, colWidths=col_widths_datos_economicos)
            datos_economicos_table.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#001978")),  # Texto de la cabecera en Azul
                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Inter'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),         
                ('BOTTOMPADDING', (0, 0), (-1, 0), 2),        
                ('TOPPADDING', (0, 0), (-1, 0), 2),       
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),        
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor("#001978")),        
                ('LINEBELOW', (0, 1), (-1, -1), 0.5, HexColor("#DDDCDC")),
            ]))
            story.append(datos_economicos_table)

        #########################################
        #             Tabla de Actuaciones      #
        #########################################

        if expediente_data.get("actuaciones"):
            story.append(Spacer(1, 0.1*inch))
            actuaciones_title = Paragraph("Actuaciones", section_title_style)
            story.append(actuaciones_title)
            story.append(Spacer(1, 0.1*inch))

            actuaciones_data = [["Fecha", "Asunto", "Responsable", "Etapa", "Facturable", "Importe", "Duración"]]
            for actuacion in expediente_data.get("actuaciones", []):
                actuaciones_data.append([
                    Paragraph(str(actuacion.get("fecha", "")), normal_style),
                    Paragraph(actuacion.get("asunto", ""), normal_style),
                    Paragraph(actuacion.get("responsable", ""), normal_style),
                    Paragraph(actuacion.get("etapa", ""), normal_style),
                    Paragraph(str(actuacion.get("facturable", "")), normal_style),
                    Paragraph(str(actuacion.get("importe", "")), normal_style),
                    Paragraph(actuacion.get("duracion", ""), normal_style)
                ])

            col_widths_actuaciones = [table_width * 0.14, table_width * 0.25, table_width * 0.14, table_width * 0.14, table_width * 0.1, table_width * 0.115, table_width * 0.115]

            actuaciones_table = Table(actuaciones_data, colWidths=col_widths_actuaciones)
            actuaciones_table.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#001978")),  # Blue header text
                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Inter'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),         
                ('BOTTOMPADDING', (0, 0), (-1, 0), 2),        
                ('TOPPADDING', (0, 0), (-1, 0), 2),       
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),        
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor("#001978")),        
                ('LINEBELOW', (0, 1), (-1, -1), 0.5, HexColor("#DDDCDC")),
            ]))
            story.append(actuaciones_table)

        #########################################
        #            Tabla de Recobros          #
        #########################################
        
        if expediente_data.get("recobros"):
            story.append(Spacer(1, 0.1*inch))
            recobros_title = Paragraph("Saldo", section_title_style)
            story.append(recobros_title)
            story.append(Spacer(1, 0.1*inch))

            # Resumen de cantidades - One table, three columns
            data_cantidades = [[
                Paragraph(f"<font size='8' color='#262626'><b>Cuantía</b></font><br/><font size='10' color='#001978'><b>{expediente_data.get('cuantia', '0.00')}</b></font>", normal_style_centered),
                Paragraph(f"<font size='8' color='#262626'><b>Intereses</b></font><br/><font size='10' color='#001978'><b>{expediente_data.get('intereses', '0.00')}</b></font>", normal_style_centered),
                Paragraph(f"<font size='8' color='#262626'><b>Saldo</b></font><br/><font size='10' color='#001978'><b>{expediente_data.get('saldo', '0.00')}</b></font>", normal_style_centered)
            ]]

            col_widths_cantidades = [table_width * 0.3333, table_width * 0.3333, table_width * 0.3333]  # Adjust widths as needed
            table_cantidades = Table(data_cantidades, colWidths=col_widths_cantidades, hAlign='LEFT')
            table_cantidades.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Inter'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('BOX', (0, 0), (-1, -1), 0.5, HexColor("#DDDCDC")),  # Add border
                ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor("#DDDCDC")),  # Add border

            ]))
            story.append(table_cantidades)
            story.append(Spacer(1, 0.1*inch))


            recobros_data = [["Tipo", "Fecha", "Descripción", "Haber", "Saldo"]]
            for recobro in expediente_data.get("recobros", []):
                recobros_data.append([
                    Paragraph(recobro.get("Tipo", ""), normal_style),
                    Paragraph(str(recobro.get("Fecha", "")), normal_style),
                    Paragraph(recobro.get("Descripcion", ""), normal_style),
                    Paragraph(str(recobro.get("Haber", "")), normal_style),
                    Paragraph(str(recobro.get("Saldo", "")), normal_style)
                ])

            col_widths_recobros = [table_width * 0.15, table_width * 0.15, table_width * 0.4, table_width * 0.15, table_width * 0.15]

            recobros_table = Table(recobros_data, colWidths=col_widths_recobros)
            recobros_table.setStyle(TableStyle([
                # Remove the background color from the header
                #('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#001978")),  # Blue header text
                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Inter'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # Set font size to 8 for all cells
                ('BOTTOMPADDING', (0, 0), (-1, 0), 2),  # Reduced bottom padding
                ('TOPPADDING', (0, 0), (-1, 0), 2),  # Reduced top padding
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'), # Align text to the top
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor("#001978")), # Add line below head
                ('LINEBELOW', (0, 1), (-1, -1), 0.5, HexColor("#DDDCDC")),  # Add lines between data rows

            ]))
            story.append(recobros_table)

        # Agregar un salto de página después de cada expediente
        story.append(PageBreak())
    # Construir el PDF
    doc.build(story)
    buffer.seek(0)  # Regresar al inicio del buffer
    return buffer