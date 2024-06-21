import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from PIL import Image, ImageTk 
import pygame
import threading

class AgregarCliente():
    """
    Clase para gestionar la interfaz de usuario y funcionalidades relacionadas con la adición de clientes.

    Attributes:
        - No tiene atributos públicos definidos directamente en esta clase.

    """
    
    def agregarCliente(self, event=None):
        """
        Agrega un cliente utilizando los datos ingresados en los campos de entrada.

        Args:
            event (tk.Event, optional): Evento que desencadena la llamada a esta función. Defaults to None.
        """
        self.corresponsal.ingresarCliente(self.txtCedula.get(), self.txtNombre.get(), self.txtApellido.get(), self.txtTelefono.get(), self.txtEmail.get())
        self.Limpiar()

    def Limpiar(self, event=None):
        """
        Limpia todos los campos de entrada y deshabilita el botón de guardar.

        Args:
            event (tk.Event, optional): Evento que desencadena la llamada a esta función. Defaults to None.
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
        self.btnGuardar.config(state="disabled")
        self.btnBuscar.config(state="normal")
      

    def salirSistema(self, event=None):
        """
        Pregunta al usuario si está seguro de salir y cierra la ventana si la respuesta es afirmativa.

        Args:
            event (tk.Event, optional): Evento que desencadena la llamada a esta función. Defaults to None.
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "Esta seguro de Salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass

    def mostrarAyuda(self, event):
        """
        Muestra un mensaje de ayuda al usuario.

        Args:
            event (tk.Event): Evento que desencadena la llamada a esta función.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe diligenciar todos los campos, luego presione el botón crear.")

    def buscarCliente(self, event=None):
        """
        Busca un cliente utilizando el número de cédula ingresado y gestiona las acciones correspondientes según el resultado.

        Args:
            event (tk.Event, optional): Evento que desencadena la llamada a esta función. Defaults to None.
        """
        cliente = self.corresponsal.buscarCliente(self.txtCedula.get())
        if cliente is None:
            self.Correcto()
            self.btnBuscar.config(state="disabled")
            self.txtNombre.config(state="normal")
            self.txtNombre.delete(0, "end")
            self.txtApellido.config(state="normal")
            self.txtApellido.delete(0, "end")
            self.txtTelefono.config(state="normal")
            self.txtTelefono.delete(0, "end")
            self.txtEmail.config(state="normal")
            self.txtEmail.delete(0, "end")

        else:
            self.Error()
            messagebox.showinfo("Error", "El número de cédula ya se encuentra registrado")
            self.Limpiar()

    def validarCedula(self, event):
        """
        Valida y gestiona la entrada del número de cédula del cliente.

        Args:
            event (tk.Event): Evento de teclado que desencadena la validación.
        """
        caracter = event.keysym
        if caracter.isdigit():
            self.txtCedula.configure(background='#90EE90')
        else:
            self.txtCedula.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtCedula.delete(len(self.txtCedula.get()) - 1, END)

        if len(self.txtCedula.get()) >= 8:
            self.btnBuscar.config(state="normal")
        else:
            self.btnBuscar.config(state="disabled")

    def validarNombre(self, event):
        """
        Valida y gestiona la entrada del nombre del cliente.

        Args:
            event (tk.Event): Evento de teclado que desencadena la validación.
        """
        caracter = event.keysym
        if caracter.isalpha():
            self.txtNombre.configure(background='#90EE90')
        else:
            self.txtNombre.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtNombre.delete(len(self.txtNombre.get()) - 1, END)


    def validarApellido(self, event):
        """
        Valida y gestiona la entrada del apellido del cliente.

        Args:
            event (tk.Event): Evento de teclado que desencadena la validación.
        """
        caracter = event.keysym
        if caracter.isalpha():
            self.txtApellido.configure(background='#90EE90')
        else:
            self.txtApellido.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtApellido.delete(len(self.txtApellido.get()) - 1, END)

    def validarTelefono(self, event):
        """
        Valida y gestiona la entrada del número de teléfono del cliente.

        Args:
            event (tk.Event): Evento de teclado que desencadena la validación.
        """
        caracter = event.keysym
        if caracter.isdigit():
            self.txtTelefono.configure(background='#90EE90')
        else:
            self.txtTelefono.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtTelefono.delete(len(self.txtTelefono.get()) - 1, END)

    def validarEmail(self, event):
        """
        Valida y gestiona la entrada del correo electrónico del cliente.

        Args:
            event (tk.Event): Evento de teclado que desencadena la validación.
        """
        input_text = self.txtEmail.get()
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.@")
        is_valid = all((char in valid_chars for char in input_text))
        
        if is_valid:
            self.txtEmail.configure(background='#90EE90')
        else:
            self.txtEmail.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtEmail.delete(len(self.txtEmail.get()) - 1, END)
        if (len(self.txtCedula.get()) >= 8 and len(self.txtNombre.get()) >= 3 and len(self.txtApellido.get()) >= 4 and len(self.txtTelefono.get()) >= 8 and len(self.txtEmail.get()) >= 5):
            self.btnGuardar.config(state="normal") 
        else:
            self.btnGuardar.config(state="disabled")  

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

    def Pregunta(self):
        """
        Reproduce un sonido de pregunta para confirmar una acción con el usuario.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Ayuda(self):
        """
        Reproduce un sonido de ayuda para proporcionar asistencia al usuario.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\ayuda.mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Limpiar_Sonido(self):
        """
        Reproduce un sonido al limpiar los campos de entrada.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\limpiar.mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()
    
    def __init__(self, menu, corresponsal):
        self.ventana = tk.Toplevel(menu)
        self.ventana.title("Agregar Cliente")
        self.ventana.config(width=300, height=300)
        self.ventana.resizable(0,0)
        
        self.corresponsal = corresponsal
        
        self.lblTitulo = tk.Label(self.ventana, text="Crear Usuario")
        self.lblTitulo.place(relx= 0.5, rely=0.1, anchor="center")
        
        self.lblCedula = tk.Label(self.ventana, text="Cédula*:")
        self.lblCedula.place(relx= 0.07, rely=0.2)
        self.txtCedula = tk.Entry(self.ventana, width=25)
        self.txtCedula.place(relx= 0.3, rely=0.2, width= 150, height= 25)
        Tooltip(self.txtCedula, "Ingrese la cédula del cliente")
        self.txtCedula.bind("<KeyRelease>", self.validarCedula)

        self.lblNombre = tk.Label(self.ventana, text="Nombres*:")
        self.lblNombre.place(relx= 0.07, rely=0.3)
        self.txtNombre = tk.Entry(self.ventana, width=25)
        self.txtNombre.place(relx= 0.3, rely=0.3, width= 150, height= 25)
        Tooltip(self.txtNombre, "Ingrese el nombre del cliente")
        self.txtNombre.bind("<KeyRelease>", self.validarNombre)

        self.lblApellido = tk.Label(self.ventana, text="Apellidos*:")
        self.lblApellido.place(relx= 0.07, rely=0.4)
        self.txtApellido = tk.Entry(self.ventana, width=25)
        self.txtApellido.place(relx= 0.3, rely=0.4, width= 150, height= 25)
        Tooltip(self.txtApellido, "Ingrese el telefono del cliente")
        self.txtApellido.bind("<KeyRelease>", self.validarApellido)

        self.lblTelefono = tk.Label(self.ventana, text="Telefono*:")
        self.lblTelefono.place(relx= 0.07, rely=0.5)
        self.txtTelefono = tk.Entry(self.ventana, width=25)
        self.txtTelefono.place(relx= 0.3, rely=0.5, width= 150, height= 25)
        Tooltip(self.txtTelefono, "Ingrese el telefono del cliente")
        self.txtTelefono.bind("<KeyRelease>", self.validarTelefono)
    
        self.lblEmail = tk.Label(self.ventana, text="Email*:")
        self.lblEmail.place(relx= 0.07, rely=0.6)
        self.txtEmail = tk.Entry(self.ventana, width=25)
        self.txtEmail.place(relx= 0.3, rely=0.6, width= 150, height= 25)
        Tooltip(self.txtEmail, "Ingrese el email del cliente")
        self.txtEmail.bind("<KeyRelease>", self.validarEmail)

        iconoBuscar = Image.open(r"iconos\encontrar.png")
        iconoBuscar = iconoBuscar.resize((15, 15))
        self.iconoBuscar = ImageTk.PhotoImage(iconoBuscar)
        self.btnBuscar = tk.Button(self.ventana, image=self.iconoBuscar, text=" Buscar", compound="left", state="disabled",  command=self.buscarCliente)
        self.btnBuscar.place(relx=0.80, rely=0.2)
        Tooltip(self.btnBuscar, "Presione para buscar el número de cédula!\nAlt+b")
        self.btnBuscar.bind('<Button-1>', self.buscarCliente)
        self.ventana.bind('<Alt-b>', self.buscarCliente)

        iconoguardar = Image.open(r"iconos\anadir.png")
        iconoguardar = iconoguardar.resize((20, 20))
        self.iconoguardar = ImageTk.PhotoImage(iconoguardar)
        self.btnGuardar = tk.Button(self.ventana, image=self.iconoguardar, text=" Agregar", compound="left", state="disabled", command=lambda: self.agregarCliente())
        self.btnGuardar.place(relx= 0.55, rely=0.85, anchor="center")
        Tooltip(self.btnGuardar, "Presione para agregar un nuevo Cliente!\nAlt+g")
        self.ventana.bind("<Alt-g>", self.agregarCliente) 

        iconoLimpiar = Image.open(r"iconos\borrar.png")
        iconoLimpiar = iconoLimpiar.resize((20, 20))
        self.iconoLimpiar = ImageTk.PhotoImage(iconoLimpiar)
        self.btnLimpiar = tk.Button(self.ventana, image=self.iconoLimpiar, text=" Limpiar", compound="left", command=lambda:self.Limpiar())
        self.btnLimpiar.place(relx= 0.2, rely=0.85, anchor="center")
        Tooltip(self.btnLimpiar, "Presione para limpiar los campos!\nAlt+l")
        self.ventana.bind("<Alt-l>", self.Limpiar)  

        iconoSalir = Image.open(r"iconos\cerrar-sesion.png")
        iconoSalir = iconoSalir.resize((20, 20))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        self.btnSalir = tk.Button(self.ventana, image=self.iconoSalir, text=" Salir", compound="left", command=lambda: self.salirSistema())
        self.btnSalir.place(relx=0.85, rely=0.85, anchor="center")
        Tooltip(self.btnSalir, "Presione para salir del sistema!\nAlt+s")
        self.ventana.bind("<Alt-s>", self.salirSistema)  
        
        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.ventana, image=self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-35, y=15, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+a")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-a>', self.mostrarAyuda)
  
        self.ventana.mainloop()

