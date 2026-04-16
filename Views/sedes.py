import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Canvas, Scrollbar, messagebox

#Clase encargada de registrar nuevas sedes
class Sedes(ctk.CTkFrame):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager

        messagebox.showinfo("por implementar......................","...")