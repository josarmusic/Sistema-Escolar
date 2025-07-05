from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
import os

def exportar_horario_deisy():
    nombre_docente = "DEISY MORILLO"
    materia = "PROYECTO"
    jornada = "TARDE"
    nombre_archivo = "Horario_DeisyMorillo.pdf"

    # Datos del logo
    logo_path = "logo_upe.png"  # Asegúrate que sea fondo transparente y esté en tu carpeta
    if not os.path.exists(logo_path):
        print("⚠️ Logo no encontrado. Asegúrate de tener logo_upe.png en la carpeta.")
        return

    # Bloques y días según tu formato
    dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
    bloques = [
        ("12:40pm - 1:20pm", ["PROYECTO 5TO B", "PROYECTO 4TO A", "PROYECTO 5TO A", "PROYECTO 5TO A", "PROYECTO 5TO B"]),
        ("1:20pm - 2:00pm",  ["", "", "", "", ""]),
        ("2:00pm - 2:40pm",  ["PROYECTO 5TO A", "PROYECTO 4TO B", "PROYECTO 5TO B", "PROYECTO 4TO B", "PROYECTO 5TO A"]),
        ("2:40pm - 3:20pm",  ["", "", "", "", ""]),
        ("3:20pm - 3:30pm",  ["RECESO", "RECESO", "RECESO", "RECESO", "RECESO"]),
        ("3:30pm - 4:10pm",  ["PROYECTO 4TO A", "PLANIFICACIÓN", "PROYECTO 4TO A", "PLANIFICACIÓN", ""]),
        ("4:10pm - 4:50pm",  ["", "", "", "", ""]),
        ("4:50pm - 5:30pm",  ["PROYECTO 4TO B", "PROYECTO 5TO B", "PROYECTO 4TO A", "", ""]),
    ]

    totales = {
        "Horas de Proyecto": "32 hrs",
        "Horas de Planificación": "4 hrs",
        "Almuerzo y Acto Cívico": "4 hrs",
        "Total Semanal": "40 HORAS"
    }

    # Preparar PDF
    c = canvas.Canvas(nombre_archivo, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Logo
    c.drawImage(logo_path, 2*cm, height - 4*cm, width=3.5*cm, preserveAspectRatio=True, mask='auto')

    # Encabezado
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 2*cm, f"HORARIO DEL DOCENTE: {nombre_docente}")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 3*cm, f"MATERIA: {materia} | JORNADA: {jornada}")

    # Tabla de horario
    data = [["HORA"] + dias]
    for bloque, actividades in bloques:
        data.append([bloque] + actividades)

    tabla = Table(data, colWidths=[4*cm] + [6*cm]*5)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (0,0), (-1,-1), 9)
    ]))
    tabla.wrapOn(c, width, height)
    tabla.drawOn(c, 2*cm, height - 12*cm)

    # Totales abajo
    y = height - 13.8*cm - len(bloques)*1.1*cm
    for label, valor in totales.items():
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2*cm, y, f"{label}: {valor}")
        y -= 1*cm

    c.showPage()
    c.save()
    print(f"✅ PDF generado: {nombre_archivo}")