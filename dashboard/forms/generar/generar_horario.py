import sqlite3
import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from dashboard.forms.generar.exportar_pdf import exportar_horario_deisy
from dashboard.forms.generar.generar_horario_por_cedula import generar_horario_por_cedula

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

def crear_tabla_horario_resultado():
    with sqlite3.connect("asignaciones.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS horario_resultado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_docente TEXT,
                id_materia TEXT,
                id_seccion TEXT,
                dia TEXT,
                id_bloque INTEGER,
                hora_inicio TEXT,
                hora_fin TEXT
            )
        """)

def crear_tabla_bloques_horarios():
    with sqlite3.connect("asignaciones.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bloques_horarios (
                id_bloque INTEGER PRIMARY KEY AUTOINCREMENT,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL
            )
        """)

def generar_horario():
    try:
        crear_tabla_horario_resultado()
        crear_tabla_bloques_horarios()

        conn = sqlite3.connect("asignaciones.db")
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM asignaciones")
        if cur.fetchone()[0] == 0:
            messagebox.showwarning("Sin asignaciones",
                "⚠️ No se puede generar el horario porque no hay asignaciones registradas.\nPrimero usa el botón 'Registrar Asignación'.")
            conn.close()
            return

        cur.execute("SELECT COUNT(*) FROM horario_resultado")
        if cur.fetchone()[0] > 0:
            respuesta = messagebox.askyesno("Horario existente",
                "Ya hay un horario generado.\n¿Deseas reemplazarlo con uno nuevo?")
            if not respuesta:
                conn.close()
                return
            cur.execute("DELETE FROM horario_resultado")

        cur.execute("SELECT id_bloque, hora_inicio, hora_fin FROM bloques_horarios ORDER BY id_bloque")
        bloques = cur.fetchall()

        cur.execute("SELECT id, docente, materia, seccion FROM asignaciones")
        asignaciones = cur.fetchall()

        horario_ocupado = {}

        for asignacion in asignaciones:
            id_asig, docente, materia, seccion = asignacion
            asignado = False

            for dia in DIAS:
                for id_bloque, hora_ini, hora_fin in bloques:
                    clave_doc = (dia, id_bloque, f"d{docente}")
                    clave_sec = (dia, id_bloque, f"s{seccion}")

                    if clave_doc in horario_ocupado or clave_sec in horario_ocupado:
                        continue

                    cur.execute("""
                        INSERT INTO horario_resultado
                        (id_docente, id_materia, id_seccion, dia, id_bloque, hora_inicio, hora_fin)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (docente, materia, seccion, dia, id_bloque, hora_ini, hora_fin))

                    horario_ocupado[clave_doc] = True
                    horario_ocupado[clave_sec] = True
                    asignado = True
                    break
                if asignado:
                    break

        conn.commit()
        conn.close()
        messagebox.showinfo("✅ Éxito", "Horario generado correctamente.")
        mostrar_horario_visual()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema generando el horario:\n{str(e)}")

def mostrar_horario_visual():
    conn = sqlite3.connect("asignaciones.db")
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT dia FROM horario_resultado ORDER BY CASE dia WHEN 'Lunes' THEN 1 WHEN 'Martes' THEN 2 WHEN 'Miércoles' THEN 3 WHEN 'Jueves' THEN 4 WHEN 'Viernes' THEN 5 END")
    dias = [fila[0] for fila in cur.fetchall()]

    cur.execute("SELECT id_bloque, hora_inicio, hora_fin FROM bloques_horarios ORDER BY id_bloque")
    bloques = cur.fetchall()

    cur.execute("SELECT dia, id_bloque, id_seccion, id_materia FROM horario_resultado")
    celdas = cur.fetchall()

    grilla = {}
    for dia, bloque, seccion, materia in celdas:
        grilla[(bloque, dia)] = f"Sec {seccion}\nMat {materia}"

    ventana = Toplevel()
    ventana.title("🗓 Horario Generado")
    ventana.configure(bg="white")

    Label(ventana, text="Horario Final", font=("Arial", 16, "bold"), bg="white").grid(
        row=0, column=0, columnspan=len(dias) + 1, pady=10)

    for i, dia in enumerate(dias):
        Label(ventana, text=dia, bg="#e0e0e0", font=("Arial", 12, "bold"),
              width=18, relief="ridge").grid(row=1, column=i + 1)

    for r, (id_bloque, ini, fin) in enumerate(bloques):
        Label(ventana, text=f"{ini}-{fin}", bg="#f0f0f0",
              relief="ridge", width=18).grid(row=r + 2, column=0)

        for c, dia in enumerate(dias):
            valor = grilla.get((id_bloque, dia), "")
            Label(ventana, text=valor, bg="white", relief="solid",
                  width=18, height=3).grid(row=r + 2, column=c + 1)

    tk.Button(ventana, text="📄 Exportar PDF de Horario", bg="#28a745", fg="white",
              font=("Arial", 10, "bold"), command=exportar_horario_deisy).grid(
        row=len(bloques) + 4, column=0, columnspan=len(dias) + 1, pady=10)

    conn.close()