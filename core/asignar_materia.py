from tkinter import Toplevel, Label, Button, messagebox, ttk
from core.asignador import asignar_bloques_automaticamente
from database.models import guardar_asignacion  # Debes tener esta función
from core.utils import carga_horaria_materias  # Diccionario con horas por materia

def FormAsignarMateria():
    ventana = Toplevel()
    ventana.title("Asignar Materia a Docente")
    ventana.geometry("400x400")

    Label(ventana, text="Cédula del Docente:").pack(pady=5)
    entry_cedula = ttk.Entry(ventana)
    entry_cedula.pack(pady=5)

    Label(ventana, text="Nombre del Docente:").pack(pady=5)
    entry_nombre = ttk.Entry(ventana)
    entry_nombre.pack(pady=5)

    Label(ventana, text="Año Escolar:").pack(pady=5)
    combo_anio = ttk.Combobox(ventana, values=["1er Año", "2do Año", "3er Año", "4to Año", "5to Año", "6to Año"], state="readonly")
    combo_anio.pack(pady=5)

    Label(ventana, text="Sección:").pack(pady=5)
    combo_seccion = ttk.Combobox(ventana, values=["A", "B", "C"], state="readonly")
    combo_seccion.pack(pady=5)

    Label(ventana, text="Materia:").pack(pady=5)
    combo_materia = ttk.Combobox(ventana, values=list(carga_horaria_materias.keys()), state="readonly")
    combo_materia.pack(pady=5)

    Label(ventana, text="Turno:").pack(pady=5)
    combo_turno = ttk.Combobox(ventana, values=["MAÑANA", "TARDE"], state="readonly")
    combo_turno.pack(pady=5)

    def asignar():
        cedula = entry_cedula.get()
        nombre = entry_nombre.get()
        anio = combo_anio.get()
        seccion = combo_seccion.get()
        materia = combo_materia.get()
        turno = combo_turno.get()

        if "" in (cedula, nombre, anio, seccion, materia, turno):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Simular disponibilidad (en producción, esto se leería de la base de datos)
        disponibilidad = {}

        # Ejecutar asignación automática
        materias = [(materia, anio, seccion)]
        asignaciones = asignar_bloques_automaticamente(nombre, materias, turno, disponibilidad, carga_horaria_materias)

        # Guardar cada bloque asignado
        for dia, bloque, texto in asignaciones:
            guardar_asignacion(cedula, nombre, anio, seccion, materia, dia, bloque, 0, "sistema")  # "sistema" puede ser el usuario actual

        resumen = "\n".join([f"{dia} {bloque} → {texto}" for dia, bloque, texto in asignaciones])
        messagebox.showinfo("Asignación completada", f"Se asignaron los siguientes bloques:\n\n{resumen}")

    Button(ventana, text="Asignar automáticamente", command=asignar).pack(pady=20)