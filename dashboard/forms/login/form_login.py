import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'dashboard')))
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
import tkinter as tk
from dashboard.forms.master.form_master import MasterPanel
from dashboard.forms.login.form_login_designer import FormLoginDesigner
from persistence.repository.auth_user_repository import AuthUserRepository
from persistence.model import Auth_User
import util.encoding_decoding as end_dec
from dashboard.forms.registration.form import FormRegister
from tkinter import simpledialog, messagebox
from dashboard.dashboard import ejecutar_dashboard

class FormLogin(FormLoginDesigner):
    
    def __init__(self):
        self.auth_repository = AuthUserRepository()
        super().__init__()
        self.ventana.after(100, self.limpiar_campos)

    def limpiar_campos(self):
        self.usuario.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.usuario.focus_set()

    def verificar(self):
        usuarios = {
        "director": "admin123",
        "secretaria": "secret2025"
    }

        usuario = self.usuario.get().strip()
        clave = self.password.get().strip()

        if usuario in usuarios and clave == usuarios[usuario]:
            self.ventana.destroy()
            from dashboard.dashboard import ejecutar_dashboard
            ejecutar_dashboard(usuario)
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña inválidos.")

    def userRegister(self):
        master_key = simpledialog.askstring("Registro restringido", "Ingrese clave de programador:", show="*")
        if master_key == "clavesecreta2025":
            FormRegister().mainloop()
        else:
            messagebox.showwarning("Acceso denegado", "Clave incorrecta. Acción cancelada.")

    def isUser(self, user: Auth_User):
        status: bool = True
        if(user == None):
            status = False
            messagebox.showerror(message="Usuario No Registrado", title="Mensaje")
        return status
    
    def isPassword(self, password: str, user: Auth_User):
        b_password = end_dec.decrypt(user.password)
        if(password == b_password):
            self.ventana.destroy()
            ejecutar_dashboard() 
        else:
            messagebox.showerror(message="Contraseña Inválida", title="Mensaje")
    
    
class MasterPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú Principal")
        self.root.mainloop()

    def volver_al_login():
        app = FormLogin()
        app.mainloop()
    