import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import sqlite3

def generar_horario_por_cedula():
    def buscar():
        cedula = entry_cedula.get()
        if not cedula.strip():
            messagebox.showerror("Error", "Debes ingresar una cédula")
            return

        conn = sqlite3.connect("asignaciones.db")
        cur = conn.cursor()
        cur.execute("""
            SELECT dia, bloque, seccion, materia 
            FROM asignaciones 
            WHERE cedula_docente = ?
            ORDER BY 
                CASE dia 
                    WHEN 'Lunes' THEN 1 WHEN 'Martes' THEN 2 WHEN 'Miércoles' THEN 3 
                    WHEN 'Jueves' THEN 4 WHEN 'Viernes' THEN 5 ELSE 6 
                END, bloque
        """, (cedula,))
        datos = cur.fetchall()
        conn.close()

        if not datos:
            messagebox.showinfo("Sin datos", "No hay asignaciones registradas para esta cédula")
            return

        mostrar_horario(datos, cedula)

    def mostrar_horario(datos, cedula):
        ventana_resultado = Toplevel()
        ventana_resultado.title(f"🗓 Horario - Cédula {cedula}")
        ventana_resultado.configure(bg="white")

        dias_orden = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        bloques_orden = sorted(set(b for _, b, _, _ in datos))

        # Cabecera
        ttk.Label(ventana_resultado, text=f"Horario de Cédula: {cedula}", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=len(dias_orden)+1, pady=10)

        # Días
        for i, dia in enumerate(dias_orden):
            ttk.Label(ventana_resultado, text=dia, background="#e0e0e0", relief="ridge", width=15).grid(row=1, column=i+1)

        # Rellenar celdas
        for r, bloque in enumerate(bloques_orden):
            ttk.Label(ventana_resultado, text=bloque, background="#f0f0f0", width=15, relief="ridge").grid(row=r+2, column=0)
            for c, dia in enumerate(dias_orden):
                asignacion = next((f"{s}\n{m}" for d, b, s, m in datos if d == dia and b == bloque), "")
                ttk.Label(ventana_resultado, text=asignacion, width=15, relief="solid").grid(row=r+2, column=c+1)

    ventana_busqueda = Toplevel()
    ventana_busqueda.title("Buscar Docente por Cédula")
    ventana_busqueda.geometry("300x120")

    # Centramos la ventana
    ventana_busqueda.update_idletasks()
    ancho = ventana_busqueda.winfo_width()
    alto = ventana_busqueda.winfo_height()
    x = (ventana_busqueda.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_busqueda.winfo_screenheight() // 2) - (alto // 2)
    ventana_busqueda.geometry(f"+{x}+{y}")

    ttk.Label(ventana_busqueda, text="Ingresa la cédula del docente:").pack(pady=10)
    entry_cedula = ttk.Entry(ventana_busqueda)
    entry_cedula.pack(pady=5)
    entry_cedula.bind("<Return>", lambda event: buscar())
    ttk.Button(ventana_busqueda, text="🔍 Buscar", command=buscar).pack(pady=5)