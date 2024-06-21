import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from Controller.Cuenta import Cuenta
from PIL import Image, ImageTk
import pygame
import threading

class EliminarCuenta(Cuenta):
    """
    Clase que gestiona la eliminación de cuentas extendiendo la funcionalidad de la clase base Cuenta.

    Attributes:
        cedula (str): Cédula del cliente asociado a la cuenta.
        numero_cuenta (str): Número de cuenta a eliminar.
        saldo (str): Saldo actual de la cuenta.

    """

    def __init__(self, cedula="", numero_cuenta="", saldo=""):
        """
        Constructor de la clase EliminarCuenta.

        Args:
            cedula (str): Cédula del cliente asociado a la cuenta (predeterminado: "").
            numero_cuenta (str): Número de cuenta a eliminar (predeterminado: "").
            saldo (str): Saldo actual de la cuenta (predeterminado: "").

        """
        Cuenta.__init__(self, cedula, numero_cuenta, saldo)

    def mostrarAyuda(self, event):
        """
        Muestra una ventana de ayuda y reproduce un sonido de ayuda.

        Args:
            event: Evento que desencadena la llamada a la función.

        Returns:
            None
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Ingrese el número de cuenta y haga clic en el botón, luego haga clic en el botón eliminar")

    def EliminarCuenta(self, event=None):
        """
        Elimina la cuenta asociada al número de cuenta ingresado.

        Args:
            event: Evento que desencadena la llamada a la función (predeterminado: None).

        Returns:
            None
        """
        self.corresponsal.EliminarCuenta(self.txtNumeroCuenta.get())
        self.Limpiar()

    def buscarCuenta(self, event=None):
        """
        Busca la cuenta asociada al número de cuenta ingresado y muestra los detalles si existe.

        Args:
            event: Evento que desencadena la llamada a la función (predeterminado: None).

        Returns:
            None
        """
        cuenta = self.corresponsal.buscarCuenta(self.txtNumeroCuenta.get())
        if cuenta is not None:
            self.Correcto()
            self.btnBuscar.config(state="disabled")
            self.txtCedula.config(state="normal")
            self.txtCedula.delete(0, "end")
            self.txtCedula.insert(0, cuenta.cliente)
            self.txtCedula.config(state="disabled")
            self.txtSaldo.config(state="normal")
            self.txtSaldo.delete(0, "end")
            self.txtSaldo.insert(0, cuenta.saldo)
            self.txtSaldo.config(state="disabled")
            self.btnBuscar.config(state="disabled")
            self.btnEliminar.config(state="normal")
        else:
            self.Limpiar()

    def salirSistema(self, event=None):
        """
        Muestra una confirmación al usuario antes de cerrar la ventana.

        Args:
            event: Evento que desencadena la llamada a la función (predeterminado: None).

        Returns:
            None
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "¿Está seguro de salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass

    def Limpiar(self, event=None):
        """
        Limpia los campos de entrada y restablece los estados de los botones después de una operación o acción.

        Args:
            event: Evento que desencadena la llamada a la función (predeterminado: None).

        Returns:
            None
        """
        self.Limpiar_Sonido()
        self.txtCedula.config(state='normal')
        self.txtCedula.delete(0, END)
        self.txtNumeroCuenta.configure(background='white')
        self.txtNumeroCuenta.config(state='normal')
        self.txtNumeroCuenta.delete(0, END)
        self.txtSaldo.config(state='normal')
        self.txtSaldo.delete(0, END)
        self.btnBuscar.config(state="disabled")
        self.btnEliminar.config(state="disabled")

    def validarNumeroCuenta(self, event):
        """
        Valida que solo se ingresen números en el campo de número de cuenta y gestiona el estado del botón de búsqueda.

        Args:
            event: Evento de teclado que desencadena la validación.

        Returns:
            None
        """
        caracter = event.keysym
        if caracter.isdigit():
            self.txtNumeroCuenta.configure(background='#90EE90')
        else:
            self.txtNumeroCuenta.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtNumeroCuenta.delete(len(self.txtNumeroCuenta.get()) - 1, END)
        if len(self.txtNumeroCuenta.get()) >= 8:
            self.btnBuscar.config(state="normal")
        else:
            self.btnBuscar.config(state="disabled")


    def Pregunta(self):
        """
        Reproduce un sonido de pregunta utilizando Pygame en un hilo separado.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Ayuda(self):
        """
        Reproduce un sonido de ayuda utilizando Pygame en un hilo separado.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\ayuda.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Limpiar_Sonido(self):
        """
        Reproduce un sonido de limpieza utilizando Pygame en un hilo separado.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\limpiar.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Correcto(self):
        """
        Reproduce un sonido de éxito.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\correcto.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def __init__(self, menu, corresponsal):
        self.ventana = tk.Toplevel(menu)
        self.ventana.resizable(0,0)
        self.ventana.title("Eliminar cuenta")
        self.ventana.config(width=350, height=220)
        self.corresponsal = corresponsal

        self.lblTitulo = tk.Label(self.ventana, text="Eliminar Cuenta")
        self.lblTitulo.place(relx= 0.5, rely=0.1, anchor="center")
        
        self.lblNumeroCuenta = tk.Label(self.ventana, text="Numero de Cta:")
        self.lblNumeroCuenta.place(relx= 0.1, rely=0.2)
        self.txtNumeroCuenta = tk.Entry(self.ventana, width=25)
        self.txtNumeroCuenta.place(relx= 0.37, rely=0.2, width= 150, height= 25)
        self.txtNumeroCuenta.bind("<KeyRelease>", self.validarNumeroCuenta)
        Tooltip(self.txtNumeroCuenta, "Ingrese el número de cuenta del cliente")

        self.lblCedula = tk.Label(self.ventana, text="Cédula:")
        self.lblCedula.place(relx= 0.1, rely=0.4)
        self.txtCedula = tk.Entry(self.ventana, width=25)
        self.txtCedula.place(relx= 0.37, rely=0.4, width= 150, height= 25)
        self.lblSaldo = tk.Label(self.ventana, text="Saldo:")
        self.lblSaldo.place(relx= 0.1, rely=0.6)
        self.txtSaldo = tk.Entry(self.ventana, width=25)
        self.txtSaldo.place(relx= 0.37, rely=0.6, width= 150, height= 25)

        iconoEliminar = Image.open(r"iconos\eliminar.png")
        iconoEliminar = iconoEliminar.resize((20, 20))
        self.iconoEliminar = ImageTk.PhotoImage(iconoEliminar)
        self.btnEliminar = tk.Button(self.ventana, image=self.iconoEliminar, text="Eliminar", state="disabled", compound="left", command=lambda: self.EliminarCuenta())
        self.btnEliminar.place(relx= 0.5, rely=0.9, anchor="center")
        Tooltip(self.btnEliminar, "Presione para eliminar la cuenta!\nAlt+e")
        self.ventana.bind("<Alt-e>", self.EliminarCuenta)

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