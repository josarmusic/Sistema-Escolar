import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import _mysql_connector

conn = _mysql_connector("sistema_escolar.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(asignaciones)")
columnas = cursor.fetchall()
print("Columnas:", columnas)

cursor.execute("SELECT * FROM asignaciones")
datos = cursor.fetchall()
print("Datos:", datos)

conn.close()

def consultar_asignaciones():
    ventana = tk.Toplevel()
    ventana.title("Consultar Asignaciones")
    ventana.geometry("900x500")
    ventana.configure(bg="#f0f0f0")

    # Etiqueta de filtro
    tk.Label(ventana, text="Buscar por Cédula:", bg="#f0f0f0").pack(pady=5)
    entrada_busqueda = tk.Entry(ventana, width=30)
    entrada_busqueda.pack()

    # Tabla
    columnas = ("cedula", "docente", "materia", "dia", "turno", "aula")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=120)
    tabla.pack(expand=True, fill="both", pady=10)

    import mysql.connector

    def buscar():
        cedula = entrada_busqueda.get()
        tabla.delete(*tabla.get_children())  # Limpiar tabla

        try:
            conn = mysql.connector.connect(
                host="localhost",           # Cambia si tu servidor no es local
                user="tu_usuario_mysql",    # Ej: "root"
                password="tu_contraseña",   # Ej: "1234"
                database="sistema_escolar"  # El nombre de tu base de datos
            )
            cursor = conn.cursor()

            if cedula:
                cursor.execute("""
                    SELECT id_docente, id_materia, id_seccion 
                    FROM asignaciones 
                    WHERE id_docente LIKE %s
                """, ('%' + cedula + '%',))
            else:
                cursor.execute("SELECT id_docente, id_materia, id_seccion FROM asignaciones")

            resultados = cursor.fetchall()
            for fila in resultados:
                tabla.insert("", "end", values=fila)

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar: {e}")

    tk.Button(ventana, text="Buscar", command=buscar).pack(pady=5)

    ventana.mainloop()