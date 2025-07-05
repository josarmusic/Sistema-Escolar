import tkinter as tk
from dashboard.forms.login import form_login

def volver_al_login():
    app = form_login.FormLogin()
    app.mainloop()