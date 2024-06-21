import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from Controller.Cuenta import Cuenta
import random
from Model.ConexionUsuario import ConexionUsuario
from PIL import Image, ImageTk
import sqlite3
import pygame
import threading

class crearCuenta(Cuenta):
    """
    Clase para la creación y gestión de cuentas en el sistema de corresponsales.
    Hereda de la clase Cuenta.

    Attributes:
        Se heredan los atributos de la clase Cuenta:
            - cedula (str): El número de cédula del cliente asociado a la cuenta.
            - numero_cuenta (str): El número único de la cuenta.
            - saldo (str): El saldo actual de la cuenta.
    """

    def __init__(self, cedula="", numero_cuenta="", saldo=""):
        """
        Inicializa una nueva instancia de crearCuenta.

        Args:
            cedula (str): El número de cédula del cliente asociado a la cuenta.
            numero_cuenta (str): El número único de la cuenta.
            saldo (str): El saldo actual de la cuenta.
        """
        Cuenta.__init__(self, cedula, numero_cuenta, saldo)

    def mostrarAyuda(self, event):
        """
        Muestra un mensaje de ayuda y reproduce un sonido de ayuda al presionar un botón.

        Args:
            event: El evento asociado al botón de ayuda.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe introducir el número de cédula y luego presionar el botón 'crear'.")

    def CrearCuenta(self, event=None):
        """
        Crea una nueva cuenta asociada al cliente con la cédula ingresada y muestra un mensaje de éxito.

        Args:
            event: El evento asociado al botón de crear cuenta.
        """
        self.corresponsal.ingresarCuenta(self.txtCedula.get(), self.txtNumeroCuenta.get(), self.txtSaldo.get())
        self.Limpiar()

    def salirSistema(self, event=None):
        """
        Pregunta al usuario si está seguro de salir del sistema y cierra la ventana si la respuesta es afirmativa.

        Args:
            event: El evento asociado al botón de salir del sistema.
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "¿Está seguro de salir?")
        if respuesta == "yes":
            self.ventana.destroy()

    def buscarCuenta(self, event=None):
        """
        Busca una cuenta asociada al cliente con la cédula ingresada.
        Si no existe, genera un número de cuenta único y muestra los campos para ingresar saldo y crear la cuenta.

        Args:
            event: El evento asociado al botón de buscar cuenta.
        """
        cuenta = self.corresponsal.buscarCuenta(self.txtCedula.get())
        if cuenta is None:
            self.Correcto()
            numero_cuenta = self.generarNumeroCuenta()
            saldo = 0
            self.btnBuscar.config(state="disabled")
            self.txtNumeroCuenta.config(state="normal")
            self.txtNumeroCuenta.delete(0, "end")
            self.txtNumeroCuenta.insert(0, numero_cuenta)
            self.txtNumeroCuenta.config(state="disabled")
            self.txtSaldo.config(state="normal")
            self.txtSaldo.delete(0, "end")
            self.txtSaldo.insert(0, saldo)
            self.txtSaldo.config(state="disabled")
            self.btnBuscar.config(state="disabled")
            self.btncrear.config(state="normal")
        else:
            self.Error()
            self.Limpiar()

    def generarNumeroCuenta(self):
        """
        Genera un número de cuenta único y verifica su disponibilidad en la base de datos.

        Returns:
            int: Número de cuenta generado y verificado como único.
        """
        miConexion = ConexionUsuario()
        miConexion.crearConexion()
        con = miConexion.getConexion()
        cursor = con.cursor()
        while True:
            try:
                numero_cuenta = random.randint(100000000, 9999999999)
                cursor.execute("SELECT numero_cuenta FROM cuenta WHERE numero_cuenta = ?", (numero_cuenta,))
                resultado = cursor.fetchone()
                if resultado is None:
                    return numero_cuenta
            except sqlite3.IntegrityError as e:
                continue
            finally:
                miConexion.cerrarConexion()

    def Limpiar(self, event=None):
        """
        Limpia los campos de entrada y restablece los estados de los botones para buscar y crear cuenta.
        
        Args:
            event: El evento asociado al botón de limpiar campos.
        """
        self.Limpiar_Sonido()
        self.txtCedula.delete(0, END)
        self.txtCedula.configure(background='white')
        self.txtNumeroCuenta.config(state="normal")
        self.txtNumeroCuenta.delete(0, END)
        self.txtSaldo.config(state="normal")
        self.txtSaldo.delete(0, END)
        self.btnBuscar.config(state="disabled")
        self.btncrear.config(state="disabled")

    def validarCedula(self, event):
        """
        Valida que solo se ingresen dígitos en el campo de cédula y habilita el botón de buscar cuando se alcanza la longitud mínima.
        
        Args:
            event: El evento asociado a la entrada en el campo de cédula.
        """
        caracter = event.keysym 
        if caracter.isdigit(): 
            self.txtCedula.configure(background='#90EE90')
        else:
            self.txtCedula.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":  
                self.txtCedula.delete(len(self.txtCedula.get())-1, END) 

        if len(self.txtCedula.get()) >= 8:
            self.btnBuscar.config(state="normal") 
        else:
            self.btnBuscar.config(state="disabled")  

    def Pregunta(self):
        """
        Reproduce un sonido de pregunta al realizar una pregunta al usuario.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Ayuda(self):
        """
        Reproduce un sonido de ayuda al solicitar ayuda al usuario.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\ayuda.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Limpiar_Sonido(self):
        """
        Reproduce un sonido de limpieza al limpiar los campos de entrada.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\limpiar.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Correcto(self):
        """
        Reproduce un sonido de éxito cuando se realiza una operación correctamente.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\correcto.mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Error(self):
        """
        Reproduce un sonido de error cuando se produce un error en la aplicación.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\error (online-audio-converter.com).mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def __init__(self, menu, corresponsal):
        self.ventana = tk.Toplevel(menu)
        self.ventana.resizable(0,0)
        self.ventana.title("Crear cuenta")
        self.ventana.config(width=350, height=200)
        self.corresponsal = corresponsal

        self.lblTitulo = tk.Label(self.ventana, text="Crear cuenta")
        self.lblTitulo.place(relx= 0.5, rely=0.1, anchor="center")
        
        self.lblCedula = tk.Label(self.ventana, text="Cédula:")
        self.lblCedula.place(relx= 0.1, rely=0.2)
        self.txtCedula = tk.Entry(self.ventana, width=25)
        self.txtCedula.place(relx= 0.37, rely=0.2, width= 150, height= 25)
        self.txtCedula.bind("<KeyRelease>", self.validarCedula)
        Tooltip(self.txtCedula, "Ingrese la cédula del cliente")

        self.lblNumeroCuenta = tk.Label(self.ventana, text="Numero de Cta:")
        self.lblNumeroCuenta.place(relx= 0.1, rely=0.4)
        self.txtNumeroCuenta = tk.Entry(self.ventana, width=25)
        self.txtNumeroCuenta.place(relx= 0.37, rely=0.4, width= 150, height= 25)
        self.lblSaldo = tk.Label(self.ventana, text="Saldo:")
        self.lblSaldo.place(relx= 0.1, rely=0.6)
        self.txtSaldo = tk.Entry(self.ventana, width=25)
        self.txtSaldo.place(relx= 0.37, rely=0.6, width= 150, height= 25)

        iconocrear = Image.open(r"iconos\anadir.png")
        iconocrear = iconocrear.resize((20, 20))
        self.iconocrear = ImageTk.PhotoImage(iconocrear)
        self.btncrear = tk.Button(self.ventana, image=self.iconocrear, text=" Agregar", compound="left", state="disabled", command=lambda: self.CrearCuenta())
        self.btncrear.place(relx= 0.5, rely=0.9, anchor="center")
        Tooltip(self.btncrear, "Presione para crear la cuenta!\nAlt+c")
        self.ventana.bind("<Alt-c>", self.CrearCuenta) 

        iconoLimpiar = Image.open(r"iconos\borrar.png")
        iconoLimpiar = iconoLimpiar.resize((20, 20))
        self.iconoLimpiar = ImageTk.PhotoImage(iconoLimpiar)
        self.btnLimpiar = tk.Button(self.ventana, image=self.iconoLimpiar, text=" Limpiar", compound="left", command=lambda:self.Limpiar())
        self.btnLimpiar.place(relx= 0.2, rely=0.9, anchor="center")
        Tooltip(self.btnLimpiar, "Presione para limpiar los campos!\nAlt+l")
        self.ventana.bind("<Alt-l>", self.Limpiar)  

        iconoSalir = Image.open(r"iconos\cerrar-sesion.png")
        iconoSalir = iconoSalir.resize((20, 20))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        self.btnSalir = tk.Button(self.ventana, image=self.iconoSalir, text=" Salir", compound="left", command=lambda: self.salirSistema())
        self.btnSalir.place(relx=0.8, rely=0.9, anchor="center")
        Tooltip(self.btnSalir, "Presione para salir del sistema!\nAlt+s")
        self.ventana.bind("<Alt-s>", self.salirSistema)  

        iconoBuscar = Image.open(r"iconos\encontrar.png")
        iconoBuscar = iconoBuscar.resize((15, 15))
        self.iconoBuscar = ImageTk.PhotoImage(iconoBuscar)
        self.btnBuscar = tk.Button(self.ventana, image=self.iconoBuscar, text=" Buscar", compound="left", state="disabled", command=self.buscarCuenta)
        self.btnBuscar.place(relx=0.82, rely=0.2)
        Tooltip(self.btnBuscar, "Presione para buscar el número de cuenta!\nAlt+b")
        self.btnBuscar.bind('<Button-1>', self.buscarCuenta)
        self.ventana.bind('<Alt-b>', self.buscarCuenta)

        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.ventana, image=self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-30, y=10, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+a")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-a>', self.mostrarAyuda)



        self.ventana.mainloop()