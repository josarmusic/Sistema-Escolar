from tkinter import Toplevel, Label, Button, messagebox, ttk, IntVar
import sqlite3
from core.asignador import asignar_bloques_automaticamente
from core.utils import carga_horaria_materias
from database.models import guardar_asignacion

def crear_formulario_asignacion():
    ventana = Toplevel()
    ventana.title("Asignar Materia Automáticamente")
    ventana.geometry("450x400")
    ventana.configure(bg="#f4f4f4")
    ventana.resizable(False, False)

    pensum = {
        "1er Año": ["Castellano", "Biología", "Matemática"],
        "2do Año": ["Inglés", "Física", "Historia"],
        "3er Año": ["Química", "Geografía", "Lengua"],
        "4to Año": ["Lengua", "Educación Física", "Matemática"],
        "5to Año": ["Proyecto", "Lengua", "Matemática"],
        "6to Año": ["Proyecto", "Vinculación", "Matemática"]
    }

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True)

    campos = {
        "Cédula del Docente": ttk.Entry(frame),
        "Nombre del Docente": ttk.Entry(frame),
        "Año Escolar": ttk.Combobox(frame, values=list(pensum.keys()), state="readonly"),
        "Sección": ttk.Combobox(frame, values=["A", "B", "C"], state="readonly"),
        "Materia": ttk.Combobox(frame, state="readonly"),
        "Turno": ttk.Combobox(frame, values=["MAÑANA", "TARDE"], state="readonly")
    }

    for i, (label, widget) in enumerate(campos.items()):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="e", pady=6, padx=10)
        widget.grid(row=i, column=1, pady=6, padx=10, sticky="we")

    def actualizar_materias(event):
        anio = campos["Año Escolar"].get()
        materias = pensum.get(anio, [])
        campos["Materia"]["values"] = materias
        campos["Materia"].set("")

    campos["Año Escolar"].bind("<<ComboboxSelected>>", actualizar_materias)

    orientador_var = IntVar()
    chk_orientador = ttk.Checkbutton(frame, text="Este docente es ORIENTADOR", variable=orientador_var)
    chk_orientador.grid(row=len(campos), column=0, columnspan=2, pady=10)

    def guardar():
        datos = {k: v.get() for k, v in campos.items()}
        if "" in datos.values():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        docente = datos["Nombre del Docente"]
        cedula = datos["Cédula del Docente"]
        anio = datos["Año Escolar"]
        seccion = datos["Sección"]
        materia = datos["Materia"]
        turno = datos["Turno"]
        orientador = orientador_var.get()

        # Simular disponibilidad (en producción se leería de la base de datos)
        disponibilidad = {}

        materias_asignadas = [(materia, anio, seccion)]
        asignaciones = asignar_bloques_automaticamente(
            docente, materias_asignadas, turno, disponibilidad, carga_horaria_materias
        )

        for dia, bloque, texto in asignaciones:
            guardar_asignacion(cedula, docente, anio, seccion, materia, dia, bloque, orientador, "sistema")

        resumen = "\n".join([f"{dia} {bloque} → {texto}" for dia, bloque, texto in asignaciones])
        messagebox.showinfo("Asignación completada", f"Se asignaron los siguientes bloques:\n\n{resumen}")
        ventana.destroy()

    ttk.Button(frame, text="Asignar Automáticamente", command=guardar).grid(
        row=len(campos)+1, column=0, columnspan=2, pady=20
    )