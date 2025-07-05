import sqlite3

def guardar_asignacion(cedula, docente, anio, seccion, materia, dia, bloque, orientador, registrado_por):
    conn = sqlite3.connect("data/asignaciones.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO asignaciones 
        (cedula_docente, docente, anio, seccion, materia, dia, bloque, orientador, registrado_por)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (cedula, docente, anio, seccion, materia, dia, bloque, orientador, registrado_por))
    conn.commit()
    conn.close()

def obtener_asignaciones_docente(nombre_docente, turno):
    """
    Devuelve una lista de asignaciones en formato [(día, bloque, texto)] para el docente.
    """
    import sqlite3
    conn = sqlite3.connect("data/asignaciones.db")
    cursor = conn.cursor()

    bloques_manana = [
        "07:10am-07:50am", "07:50am-08:30am", "08:40am-09:20am", "09:20am-10:00am",
        "10:00am-10:40am", "10:40am-11:20am", "11:20am-12:00am", "12:00am-12:40am"
    ]
    bloques_tarde = [
        "12:40pm-1:20pm", "1:20pm-2:00pm", "2:00pm-2:40pm", "2:40pm-3:20pm",
        "3:30pm-4:10pm", "4:10pm-4:50pm", "4:50pm-5:30pm", "5:30pm-6:10pm"
    ]
    bloques_validos = bloques_manana if turno == "MAÑANA" else bloques_tarde

    cursor.execute("""
        SELECT dia, bloque, materia, anio, seccion
        FROM asignaciones
        WHERE docente = ?
    """, (nombre_docente,))
    filas = cursor.fetchall()
    conn.close()

    resultado = []
    for dia, bloque, materia, anio, seccion in filas:
        if bloque in bloques_validos:
            texto = f"{materia} {anio} {seccion}"
            resultado.append((dia, bloque, texto))
    return resultado