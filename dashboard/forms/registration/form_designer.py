import tkinter as tk
from tkinter import ttk
import util.generic as utl

class FormRegisterDesigner():
    
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('REGISTRO DE USUARIO')
        self.ventana.config(bg="#ff932f")
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana,600,550)

        logo =utl.leer_image("./imagenes/logoeta.png", (200, 250))

        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=120, relief=tk.SOLID, padx=10, pady=10,bg='#fcfcfc')
        frame_logo.pack(side="left",expand=tk.YES,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=logo,bg='#ff932f')
        label.place(x=0,y=0,relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=47, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="REGISTRO DE USUARIO", font=('Impact', 20), fg="#ff932f", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=200, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="top", fill=tk.BOTH, expand=True)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Monserrat', 14) ,fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Monserrat', 14))
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Monserrat', 14),fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Monserrat', 14))
        self.password.pack(fill=tk.X, padx=20,pady=10)
        self.password.config(show="*")

        etiqueta_confirmation = tk.Label(frame_form_fill, text="Confirmar Contraseña", font=('Monserrat', 14),fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_confirmation.pack(fill=tk.X, padx=20, pady=5)
        self.confirmation = ttk.Entry(frame_form_fill, font=('Monserrat', 14))
        self.confirmation.pack(fill=tk.X, padx=20,pady=10)
        self.confirmation.config(show="*")

        register = tk.Button(frame_form_fill, text="REGISTRAR", font=('Monserrat', 10),
                             bg="#ff932f", bd=0, fg="#fcfcfc", command=self.register)
        register.pack(fill=tk.X, padx=70, pady=15)
        register.bind("<Return>", (lambda event: self.register())) 
 
        self.ventana.mainloop()

    def register(self):
        print("Registro exitoso")
