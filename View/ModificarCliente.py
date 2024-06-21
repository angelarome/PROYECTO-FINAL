import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from PIL import Image, ImageTk
import pygame
import threading

class ModificarCliente():
    """
    Clase que gestiona la modificación de datos de un cliente.

    Attributes:
        ventana: Ventana principal de la interfaz de modificación.
        corresponsal: Objeto corresponsal para la gestión de clientes.

    """

    def salirSistema(self, event=None):
        """
        Muestra una pregunta de confirmación y cierra la ventana si el usuario confirma.

        Args:
            event: Evento asociado al método (opcional).
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "¿Está seguro de salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass

    def mostrarAyuda(self, event):
        """
        Muestra una ventana de ayuda y reproduce un sonido de ayuda.

        Args:
            event: Evento asociado al método.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe introducir el número de cédula, luego presionar el bóton buscar, posteriormente digite el dato que desea cambiar y presione el botón modificar.")

    def ModificarCliente(self, event=None):
        """
        Modifica los datos del cliente utilizando los valores de los campos de entrada.
        
        Args:
            event: Evento asociado al método (opcional).
        """
        self.corresponsal.modificarCliente(self.txtCedula.get(), self.txtNombre.get(), self.txtApellido.get(), self.txtTelefono.get(), self.txtEmail.get())
        self.Limpiar()

    def buscarCliente(self, event=None):
        """
        Busca un cliente por su número de cédula y muestra sus datos en los campos correspondientes.
        
        Args:
            event: Evento asociado al método (opcional).
        """
        cliente = self.corresponsal.buscarCliente(self.txtCedula.get())
        if cliente is not None:
            self.Correcto()
            self.txtNombre.config(state="normal")
            self.txtNombre.delete(0, "end")
            self.txtNombre.insert(0, cliente.nombre)
            self.txtApellido.config(state="normal")
            self.txtApellido.delete(0, "end")
            self.txtApellido.insert(0, cliente.apellido)
            self.txtTelefono.config(state="normal")
            self.txtTelefono.delete(0, "end")
            self.txtTelefono.insert(0, cliente.telefono)
            self.txtEmail.config(state="normal")
            self.txtEmail.delete(0, "end")
            self.txtEmail.insert(0, cliente.email)
            self.btnBuscar.config(state="disabled")
            self.btnModificar.config(state="normal")
        else:
            self.Limpiar()

    def Limpiar(self, event=None):
        """
        Limpia los campos de entrada y restablece los estados y configuraciones iniciales.
        
        Args:
            event: Evento asociado al método (opcional).
        """
        self.Limpiar_Sonido()
        self.txtCedula.delete(0, END)
        self.txtCedula.configure(background='white')
        self.txtNombre.config(state='normal')
        self.txtNombre.delete(0, END)
        self.txtNombre.configure(background='white')
        self.txtApellido.config(state='normal')
        self.txtApellido.delete(0, END)
        self.txtApellido.configure(background='white')
        self.txtTelefono.config(state='normal')
        self.txtTelefono.delete(0, END)
        self.txtTelefono.configure(background='white')
        self.txtEmail.config(state='normal')
        self.txtEmail.delete(0, END)
        self.txtEmail.configure(background='white')
        self.btnBuscar.config(state="disabled")
        self.btnModificar.config(state="disabled")

    def validarCedula(self, event):
        """
        Valida la entrada de caracteres en el campo de cédula y habilita el botón de búsqueda cuando se cumple la longitud mínima.
        
        Args:
            event: Evento de teclado asociado al método.
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

    def validarNombre(self, event):
        """
        Valida la entrada de caracteres en el campo de nombre.
        
        Args:
            event: Evento de teclado asociado al método.
        """
        caracter = event.keysym 
        if caracter.isalpha():
            self.txtNombre.configure(background='#90EE90')
        else:
            self.txtNombre.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtNombre.delete(len(self.txtNombre.get())-1, END)

    def validarApellido(self, event):
        """
        Valida la entrada de caracteres en el campo de apellido.
        
        Args:
            event: Evento de teclado asociado al método.
        """
        caracter = event.keysym 
        if caracter.isalpha():
            self.txtApellido.configure(background='#90EE90')
        else:
            self.txtApellido.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtApellido.delete(len(self.txtApellido.get())-1, END)

    def validarTelefono(self, event):
        """
        Valida la entrada de caracteres en el campo de teléfono.
        
        Args:
            event: Evento de teclado asociado al método.
        """
        caracter = event.keysym 
        if caracter.isdigit():
            self.txtTelefono.configure(background='#90EE90')
        else:
            self.txtTelefono.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtTelefono.delete(len(self.txtTelefono.get())-1, END)

    def validarEmail(self, event):
        """
        Valida la entrada de caracteres en el campo de email.
        
        Args:
            event: Evento de teclado asociado al método.
        """
        caracter = event.keysym 
        if caracter.isalnum():
            self.txtEmail.configure(background='#90EE90')
        else:
            self.txtEmail.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtEmail.delete(len(self.txtEmail.get())-1, END)

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

    def Ayuda(self):
        """
        Reproduce un sonido de ayuda utilizando threading para evitar bloqueos.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\ayuda.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Limpiar_Sonido(self):
        """
        Reproduce un sonido de limpieza utilizando threading para evitar bloqueos.
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
        self.ventana.title("Modificar cliente")
        self.ventana.config(width=300, height=300)
        self.corresponsal = corresponsal

        self.lblTitulo = tk.Label(self.ventana, text="Modificar Cliente")
        self.lblTitulo.place(relx= 0.5, rely=0.1, anchor="center")
        
        self.lblCedula = tk.Label(self.ventana, text="Cédula:")
        self.lblCedula.place(relx= 0.1, rely=0.2)
        self.txtCedula = tk.Entry(self.ventana, width=25)
        self.txtCedula.place(relx= 0.3, rely=0.2, width= 150, height= 25)
        self.txtCedula.bind("<KeyRelease>", self.validarCedula)
        Tooltip(self.txtCedula, "Ingrese la cédula del cliente")
        self.lblNombre = tk.Label(self.ventana, text="Nombres:")
        self.lblNombre.place(relx= 0.1, rely=0.3)
        self.txtNombre = tk.Entry(self.ventana, width=25)
        self.txtNombre.place(relx= 0.3, rely=0.3, width= 150, height= 25)
        self.txtNombre.bind("<KeyRelease>", self.validarNombre)
        self.lblApellido = tk.Label(self.ventana, text="Apellidos:")
        self.lblApellido.place(relx= 0.1, rely=0.4)
        self.txtApellido = tk.Entry(self.ventana, width=25)
        self.txtApellido.place(relx= 0.3, rely=0.4, width= 150, height= 25)
        self.txtApellido.bind("<KeyRelease>", self.validarApellido)
        self.lblTelefono = tk.Label(self.ventana, text="Telefono:")
        self.lblTelefono.place(relx= 0.1, rely=0.5)
        self.txtTelefono = tk.Entry(self.ventana, width=25)
        self.txtTelefono.place(relx= 0.3, rely=0.5, width= 150, height= 25)
        self.txtTelefono.bind("<KeyRelease>", self.validarTelefono)
        self.lblEmail = tk.Label(self.ventana, text="Email:")
        self.lblEmail.place(relx= 0.1, rely=0.6)
        self.txtEmail = tk.Entry(self.ventana, width=25)
        self.txtEmail.place(relx= 0.3, rely=0.6, width= 150, height= 25)
        self.txtEmail.bind("<KeyRelease>", self.validarEmail)
        
        iconoModificar = Image.open(r"iconos\editar.png")
        iconoModificar = iconoModificar.resize((20, 20))
        self.iconoModificar = ImageTk.PhotoImage(iconoModificar)
        self.btnModificar = tk.Button(self.ventana, image=self.iconoModificar, text="Modificar", state="disabled", compound="left", command=lambda: self.ModificarCliente())
        self.btnModificar.place(relx= 0.5, rely=0.8, anchor="center")
        Tooltip(self.btnModificar, "Presione para modificar el cliente!\nAlt+m")
        self.ventana.bind("<Alt-m>", self.ModificarCliente)

        iconoSalir = Image.open(r"iconos\cerrar-sesion.png")
        iconoSalir = iconoSalir.resize((20, 20))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        self.btnSalir = tk.Button(self.ventana, image=self.iconoSalir, text=" Salir", compound="left", command=lambda: self.salirSistema())
        self.btnSalir.place(relx=0.8, rely=0.8, anchor="center")
        Tooltip(self.btnSalir, "Presione para salir del sistema!\nAlt+s")
        self.ventana.bind("<Alt-s>", self.salirSistema)

        iconoLimpiar = Image.open(r"iconos\borrar.png")
        iconoLimpiar = iconoLimpiar.resize((20, 20))
        self.iconoLimpiar = ImageTk.PhotoImage(iconoLimpiar)
        self.btnLimpiar = tk.Button(self.ventana, image=self.iconoLimpiar, text=" Limpiar", compound="left", command=lambda:self.Limpiar())
        self.btnLimpiar.place(relx= 0.2, rely=0.8, anchor="center")
        Tooltip(self.btnLimpiar, "Presione para limpiar los campos!\nAlt+l")
        self.ventana.bind("<Alt-l>", self.Limpiar)  

        iconoBuscar = Image.open(r"iconos\encontrar.png")
        iconoBuscar = iconoBuscar.resize((15, 15))
        self.iconoBuscar = ImageTk.PhotoImage(iconoBuscar)
        self.btnBuscar = tk.Button(self.ventana, image=self.iconoBuscar, text=" Buscar", compound="left", state="disabled", command=self.buscarCliente)
        self.btnBuscar.place(relx=0.80, rely=0.2)
        Tooltip(self.btnBuscar, "Presione para buscar el número de cèdula!\nAlt+b")
        self.btnBuscar.bind('<Button-1>', self.buscarCliente)
        self.ventana.bind('<Alt-b>', self.buscarCliente)

        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.ventana, image=self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-35, y=15, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+a")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-a>', self.mostrarAyuda)

        self.ventana.mainloop()