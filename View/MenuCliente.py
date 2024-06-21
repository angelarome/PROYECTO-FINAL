import tkinter as tk
from tkinter import *
from tkinter import messagebox
from View.Deposito import Deposito
from View.Retiro import Retiro
from Tooltip import Tooltip
from PIL import Image, ImageTk
import pygame
import threading

class MenuCliente():
    """
    Clase que representa el menú principal para clientes.

    Attributes:
        ventana (tk.Toplevel): Ventana principal del menú.
        cliente (Cliente): Objeto cliente actual.
        corresponsal (Corresponsal): Objeto corresponsal para la gestión de transacciones.
        cuenta (Cuenta): Objeto cuenta asociado al cliente.
        menu (tk.Menu): Menú principal del cliente.

    """
    def salirSistema(self):
        """
        Muestra un mensaje de confirmación para salir del sistema y destruye la ventana si se confirma la salida.
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "Esta seguro de Salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass

    def Deposito(self):
        """
        Abre la ventana para realizar un depósito en la cuenta actual del cliente.
        """
        depositar = Deposito(self.ventana, None, self.cuenta, self.cliente)

    def Retiro(self):
        """
        Abre la ventana para realizar un retiro de la cuenta actual del cliente.
        """
        retiro = Retiro(self.ventana, None, self.cuenta, self.cliente)

    def mostrarAyuda(self, event):
        """
        Muestra una ventana de ayuda y reproduce un sonido de ayuda cuando se hace clic en el icono de ayuda.

        Args:
            event: Evento de clic en el icono de ayuda.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Coloca el mouse sobre el menú cascada, \n esto le permitirá ver todas las opciones del menú.")

    def Ayuda(self):
        """
        Reproduce un sonido de ayuda.

        Utiliza threading para reproducir el sonido en un hilo separado.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\ayuda.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Pregunta(self):
        """
        Reproduce un sonido de pregunta utilizando threading para evitar bloqueos.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def __init__(self, loggin, corresponsal, cuenta, cliente):
        self.ventana = tk.Toplevel(loggin)
        self.ventana.geometry("250x250")
        self.ventana.focus_set() 
        self.ventana.title("Menu Principal")
        self.ventana.resizable(0,0)
        self.cliente = cliente
        self.corresponsal = corresponsal
        self.cuenta = cuenta
        self.menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menu)
        menuTransacciones = tk.Menu(self.menu)
        self.menu.add_cascade(label="Gestionar Transacciones", menu=menuTransacciones)
        iconoRetiro = Image.open(r"iconos\cajero-automatico.png")
        iconoRetiro = iconoRetiro.resize((25, 25))
        self.iconoRetiro = ImageTk.PhotoImage(iconoRetiro)
        menuTransacciones.add_command(label="Realizar Retiro", command=lambda: self.Retiro(), image=self.iconoRetiro, compound="left")
        menuTransacciones.add_separator()
        iconoDeposito = Image.open(r"iconos\flecha.png")
        iconoDeposito = iconoDeposito.resize((25, 25))
        self.iconoDeposito = ImageTk.PhotoImage(iconoDeposito)
        menuTransacciones.add_command(label="Realizar Depósito", command=lambda: self.Deposito(), image=self.iconoDeposito, compound="left")

        salirMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Salir", menu=salirMenu)
        iconoSalir = Image.open(r"iconos\salir.png")
        iconoSalir = iconoSalir.resize((25, 25))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        salirMenu.add_command(label="Salir", command=lambda: self.salirSistema(), image=self.iconoSalir, compound="left")
        self.lblTitulo = tk.Label(self.ventana, text=f"Bienvenido {cliente.nombre} {cliente.apellido}")
        self.lblTitulo.grid(row=3, column=6)

        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.ventana, image= self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-30, y=10, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+l")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-l>', self.mostrarAyuda)


        self.ventana.mainloop()