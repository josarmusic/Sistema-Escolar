import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from dashboard.forms.crear.registrar_asignacion import crear_formulario_asignacion
from dashboard.forms.generar.generar_horario_por_cedula import generar_horario_por_cedula
from dashboard.forms.login.launcher import volver_al_login

def ejecutar_dashboard(usuario=None):
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión de Horarios")
    ventana.geometry("1024x600")
    ventana.state("zoomed")

    canvas = tk.Canvas(ventana, width=1920, height=1200, bg="#2c2f33")
    canvas.pack(fill="both", expand=True)

    # Fondo y logo institucional
    try:
        fondo_img = Image.open("imagenes/fondoeta.png")
        fondo_img = fondo_img.resize((1920, 1200))
        fondo = ImageTk.PhotoImage(fondo_img)
        canvas.create_image(0, 0, image=fondo, anchor="nw")
        ventana.fondo = fondo

        logo_img = Image.open("imagenes/logoeta.png")
        logo_img = logo_img.resize((170, 200))
        logo = ImageTk.PhotoImage(logo_img)
        canvas.create_image(680, 15, image=logo, anchor="n")
        ventana.logo = logo
    except Exception as e:
        print(f"Error cargando imágenes: {e}")

    # Títulos
    canvas.create_text(680, 220, text="ESCUELA TÉCNICA ASISTENCIAL", font=("Impact", 45, "bold"), fill="#0C0C0C")
    canvas.create_text(680, 265, text="HUGO RAFAEL CHAVEZ FRIAS", font=("Montserrat", 12), fill="black")

    # Bienvenida
    if usuario:
        canvas.create_text(135, 25, text=f"👤 Bienvenido(a), {usuario.upper()}", font=("Montserrat", 10, "bold"), fill="black")

    # Funciones de los botones
    def registrar():
        crear_formulario_asignacion()

    def consultar():
        try:
            from dashboard.forms.consultar.consultar_asignaciones import consultar_asignaciones
            consultar_asignaciones()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el módulo de consulta:\n{e}")

    def generar():
        generar_horario_por_cedula()

    def salir():
        ventana.destroy()
        volver_al_login()

    # Botones principales
    botones = [
        ("📝 Registrar Asignación", registrar),
        ("🔍 Consultar Asignaciones", consultar),
        ("⚙️ Generar Horario", generar)
    ]

    for i, (texto, comando) in enumerate(botones):
        boton = tk.Button(
            canvas,
            text=texto,
            font=("Montserrat", 13, "bold"),
            width=30,
            height=2,
            bg="#3d3d3d",
            fg="white",
            relief="flat",
            activebackground="#a5a5a5",
            cursor="hand2",
            command=comando
        )
        canvas.create_window(680, 360 + i * 80, window=boton)

    # Botón cerrar sesión
    cerrar_btn = tk.Button(
        canvas,
        text="CERRAR SESION",
        font=("Montserrat", 8, "bold"),
        bg="#4e4d4d",
        fg="white",
        width=13,
        height=1,
        relief="flat",
        activebackground="#bdbcbc",
        cursor="hand2",
        command=salir
    )
    canvas.create_window(1335, 42, window=cerrar_btn, anchor="se")

    # Pie de página
    canvas.create_text(
        1250, 700,
        text="Sistema de Gestión de Horarios — Versión 1.0\nDesarrollado por Rondón, Silva y Hernandez • Venezuela 🇻🇪",
        font=("Montserrat", 7),
        fill="gray"
    )

    ventana.mainloop()