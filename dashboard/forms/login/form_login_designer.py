import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
from dashboard.forms.master.form_master import MasterPanel

class FormLoginDesigner:


    def verificar(self):
        pass

    def userRegister(self):
        pass


    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('TONTO Y RETONTO')
        self.ventana.geometry('700x500')
        self.ventana.config(bg="#ff932f")
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana,700,500)

        logo =utl.leer_image("./imagenes/logoeta.png", (200, 250))

        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='#ff932f')
        frame_logo.pack(side="left",expand=tk.YES,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=logo,bg="#ff932f")
        label.place(x=0,y=0,relwidth=1, relheight=1)

        #frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_logo.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form

        # frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=47, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="INICIO DE SESIÓN", font=('Impact', 40), fg="#ff932f", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form,height = 40, bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Monserrat', 14) ,fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Monserrat', 14))
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Monserrat', 14),fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Monserrat', 14))
        self.password.pack(fill=tk.X, padx=20,pady=10)
        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill,text="ENTRAR",font=('Monserrat', 15,BOLD),bg='#ff932f', bd=0,fg="#fff",command=self.verificar)
        inicio.pack(fill=tk.X, padx=20,pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))

        inicio = tk.Button(frame_form_fill, text="REGISTRARSE", font=('Monserrat', 10), bg='#fcfcfc', bd=0, fg="#ff932f", command=self.userRegister)
        inicio.pack(fill=tk.X, padx=80, pady=20)
        inicio.bind("<Return>", (lambda event: self.userRegister()))
 


        #end frame_for_fill 
        self.ventana.mainloop()