from tkinter import Toplevel, Label, Button, messagebox, ttk
from database.models import obtener_asignaciones_docente
from core.generador_excel import generar_horario_docente

def FormGenerarHorario():
    ventana = Toplevel()
    ventana.title("Generar Horario Docente")
    ventana.geometry("400x300")

    Label(ventana, text="Nombre del Docente:").pack(pady=5)
    entry_nombre = ttk.Entry(ventana)
    entry_nombre.pack(pady=5)

    Label(ventana, text="Turno:").pack(pady=5)
    combo_turno = ttk.Combobox(ventana, values=["MAÑANA", "TARDE"], state="readonly")
    combo_turno.pack(pady=5)

    def generar():
        nombre = entry_nombre.get()
        turno = combo_turno.get()

        if not nombre or not turno:
            messagebox.showerror("Error", "Completa todos los campos")
            return

        # Obtener asignaciones desde la base de datos
        asignaciones = obtener_asignaciones_docente(nombre, turno)

        if not asignaciones:
            messagebox.showwarning("Sin asignaciones", "Este docente no tiene asignaciones registradas.")
            return

        # Generar el archivo Excel
        generar_horario_docente(nombre, turno, asignaciones)
        messagebox.showinfo("Éxito", f"Horario generado para {nombre}")

    Button(ventana, text="Generar Horario", command=generar).pack(pady=20)