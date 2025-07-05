def asignar_bloques_automaticamente(docente, materias_asignadas, turno, disponibilidad_secciones, carga_horaria_materias):
    """
    Asigna bloques automáticamente a un docente según disponibilidad y carga horaria.

    docente: str → Nombre del docente
    materias_asignadas: list of tuples → [(materia, año, sección)]
    turno: str → "MAÑANA" o "TARDE"
    disponibilidad_secciones: dict → Disponibilidad por sección y bloque
    carga_horaria_materias: dict → Horas semanales por materia

    return: list of tuples → [(día, bloque, texto)]
    """

    bloques_turno = {
        "MAÑANA": [
            "07:10am-07:50am", "07:50am-08:30am", "08:40am-09:20am", "09:20am-10:00am",
            "10:00am-10:40am", "10:40am-11:20am", "11:20am-12:00am", "12:00am-12:40am"
        ],
        "TARDE": [
            "12:40pm-1:20pm", "1:20pm-2:00pm", "2:00pm-2:40pm", "2:40pm-3:20pm",
            "3:30pm-4:10pm", "4:10pm-4:50pm", "4:50pm-5:30pm", "5:30pm-6:10pm"
        ]
    }

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    asignaciones = []

    for materia, anio, seccion in materias_asignadas:
        horas_necesarias = carga_horaria_materias.get(materia, 0)
        bloques_disponibles = 0

        for dia in dias_semana:
            for bloque in bloques_turno[turno]:
                clave = (anio, seccion)
                if clave not in disponibilidad_secciones:
                    disponibilidad_secciones[clave] = {d: {b: None for b in bloques_turno[turno]} for d in dias_semana}

                ocupado = disponibilidad_secciones[clave][dia][bloque]
                if ocupado is None:
                    # Asignar bloque
                    texto = f"{materia} {anio} {seccion}"
                    disponibilidad_secciones[clave][dia][bloque] = f"{materia} - {docente}"
                    asignaciones.append((dia, bloque, texto))
                    bloques_disponibles += 1
                    if bloques_disponibles == horas_necesarias:
                        break
            if bloques_disponibles == horas_necesarias:
                break

        if bloques_disponibles < horas_necesarias:
            print(f"⚠️ No se encontraron suficientes bloques para {materia} ({bloques_disponibles}/{horas_necesarias})")

    return asignaciones