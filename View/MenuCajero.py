import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from View.AgregarCliente import AgregarCliente
from View.EliminarCliente import EliminarCliente
from View.ModificarCliente import ModificarCliente
from View.crearCuenta import crearCuenta
from View.EliminarCuenta import EliminarCuenta
from View.Retiro import Retiro
from View.Deposito import Deposito
from View.GenerarReporte import GenerarReporte
from PIL import Image, ImageTk
import pygame
import threading

class MenuCajero():
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

    def mostrarAyuda(self, event):
        """
        Muestra un mensaje de ayuda sobre cómo utilizar el menú cascada.

        Args:
            event: Evento de disparo.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Coloca el mause sobre el menú cascada, \n esto le permitirá ver todas las opciones del menú.")
  
    def agregarCliente(self):
        """
        Abre la vista para agregar un nuevo cliente.
        """
        vistaAgregar = AgregarCliente(self.ventana, self.corresponsal)

    def eliminarCliente(self):
        """
        Abre la vista para eliminar un cliente existente.
        """
        eliminar = EliminarCliente(self.ventana, self.corresponsal)

    def ModificarCliente(self):
        """
        Abre la vista para modificar los datos de un cliente existente.
        """
        modificar = ModificarCliente(self.ventana, self.corresponsal)

    def CrearCuenta(self):
        """
        Abre la vista para crear una nueva cuenta.
        """
        crear = crearCuenta(self.ventana, self.corresponsal)

    def EliminarCuenta(self):
        """
        Abre la vista para eliminar una cuenta existente.
        """
        eliminar = EliminarCuenta(self.ventana, self.corresponsal)

    def Retiro(self):
        """
        Abre la vista para realizar un retiro de una cuenta.
        """
        retirar = Retiro(self.ventana, self.corresponsal)

    def Deposito(self):
        """
        Abre la vista para realizar un depósito en una cuenta.
        """
        deposito = Deposito(self.ventana, self.corresponsal)

    def GenerarReporte(self):
        """
        Abre la vista para generar un reporte de cuentas.
        """
        reporte = GenerarReporte(self.ventana)

    def Pregunta(self):
        """
        Reproduce un sonido de pregunta.

        Utiliza threading para reproducir el sonido en un hilo separado.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

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
            
    def __init__(self, loggin, corresponsal):
        self.ventana = tk.Toplevel(loggin)
        self.ventana.geometry("550x200")
        self.ventana.focus_set() 
        self.ventana.title("Menu Principal")
        self.ventana.resizable(0,0)

        self.corresponsal = corresponsal

        self.menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menu)

        self.lblTitulo = tk.Label(self.ventana, text=f"Bienvenido al corresponsal {corresponsal.nombre}")
        self.lblTitulo.place(relx= 0.5, rely=0.1, anchor="center")

        menuCliente = tk.Menu(self.menu)
        self.menu.add_cascade(label="Gestionar Clientes", menu=menuCliente)
        iconoAgregar = Image.open(r"iconos\alquiler.png")
        iconoAgregar = iconoAgregar.resize((25, 25))
        self.iconoAgregar = ImageTk.PhotoImage(iconoAgregar)
        menuCliente.add_command(label=" Registrar Cliente", command=lambda: self.agregarCliente(), image=self.iconoAgregar, compound="left")
        menuCliente.add_separator()
        iconoEliminar = Image.open(r"iconos\dejar-de-seguir.png")
        iconoEliminar = iconoEliminar.resize((25, 25))
        self.iconoEliminar = ImageTk.PhotoImage(iconoEliminar)
        menuCliente.add_command(label=" Eliminar Cliente", command=lambda: self.eliminarCliente(), image=self.iconoEliminar, compound="left")
        menuCliente.add_separator()
        iconoModificar = Image.open(r"iconos\editar-informacion.png")
        iconoModificar = iconoModificar.resize((25, 25))
        self.iconoModificar = ImageTk.PhotoImage(iconoModificar)
        menuCliente.add_command(label=" Modificar cliente", command=lambda: self.ModificarCliente(), image=self.iconoModificar, compound="left")
        menuCliente.add_separator()

        menuCuentas = tk.Menu(self.menu)#Creamos opcion de menu y ubicamos en la barra
        self.menu.add_cascade(label="Gestionar Cuentas", menu=menuCuentas)
        iconoCrear = Image.open(r"iconos\tarjeta-de-credito.png")
        iconoCrear = iconoCrear.resize((25, 25))
        self.iconoCrear = ImageTk.PhotoImage(iconoCrear)
        menuCuentas.add_command(label="Crear cuenta", command=lambda: self.CrearCuenta(), image=self.iconoCrear, compound="left")
        menuCuentas.add_separator()
        iconoEliminarC = Image.open(r"iconos\tarjeta.png")
        iconoEliminarC = iconoEliminarC.resize((25, 25))
        self.iconoEliminarC = ImageTk.PhotoImage(iconoEliminarC)
        menuCuentas.add_command(label="Eliminar cuenta", command=lambda: self.EliminarCuenta(), image=self.iconoEliminarC, compound="left")
        menuCuentas.add_separator()

        menuTransacciones = tk.Menu(self.menu)
        self.menu.add_cascade(label="Gestionar Transacciones", menu=menuTransacciones)
        iconoDeposito = Image.open(r"iconos\flecha.png")
        iconoDeposito = iconoDeposito.resize((25, 25))
        self.iconoDeposito = ImageTk.PhotoImage(iconoDeposito)
        menuTransacciones.add_command(label="Realizar deposito", command=lambda: self.Deposito(), image=self.iconoDeposito, compound="left")
        menuTransacciones.add_separator()
        iconoRetiro = Image.open(r"iconos\cajero-automatico.png")
        iconoRetiro = iconoRetiro.resize((25, 25))
        self.iconoRetiro = ImageTk.PhotoImage(iconoRetiro)
        menuTransacciones.add_command(label="Realizar retiro", command=lambda: self.Retiro(), image=self.iconoRetiro, compound="left")
        menuTransacciones.add_separator()

        menuConsultas = tk.Menu(self.menu)
        self.menu.add_cascade(label="Consultar Información", menu=menuConsultas)
        iconoReporte = Image.open(r"iconos\documento.png")
        iconoReporte = iconoReporte.resize((25, 25))
        self.iconoReporte = ImageTk.PhotoImage(iconoReporte)
        menuConsultas.add_command(label="Generar Reporte", command=lambda: self.GenerarReporte(), image=self.iconoReporte, compound="left")
        menuConsultas.add_separator()
        salirMenu = tk.Menu(self.menu)
        iconoSalir = Image.open(r"iconos\salir.png")
        iconoSalir = iconoSalir.resize((25, 25))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        self.menu.add_cascade(label= "Salir", menu = salirMenu)
        salirMenu.add_command(label= " Salir", command=lambda: self.salirSistema(), image=self.iconoSalir, compound="left")

        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.ventana, image=self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-45, y=15, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+a")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-a>', self.mostrarAyuda)


        self.ventana.mainloop()
        