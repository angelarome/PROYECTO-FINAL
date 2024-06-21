import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from PIL import Image, ImageTk
import pygame
import threading

class EliminarCliente():
    """
    Clase para manejar la funcionalidad de eliminar un cliente.

    """

    def eliminarCliente(self, event=None):
        """
        Elimina un cliente utilizando el número de cédula ingresado y luego limpia los campos.

        Args:
            event (Event, optional): Evento que desencadena la función. Defaults to None.
        """
        self.corresponsal.eliminarCliente(self.txtCedula.get())
        self.Limpiar()

    def salirSistema(self, event=None):
        """
        Muestra una confirmación al usuario para salir del sistema.

        Args:
            event (Event, optional): Evento que desencadena la función. Defaults to None.
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "¿Está seguro de salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass
    
    def validarCedula(self, event):
        """
        Valida que la entrada en el campo de cédula sea numérica y habilita el botón de buscar cuando se alcanza la longitud adecuada.

        Args:
            event (Event): Evento que desencadena la función.
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

    def buscarCliente(self, event=None):
        """
        Busca un cliente utilizando el número de cédula ingresado.

        Si se encuentra el cliente, muestra su información en los campos correspondientes y habilita el botón de eliminar.

        Args:
            event (Event, optional): Evento que desencadena la función. Defaults to None.
        """
        cliente = self.corresponsal.buscarCliente(self.txtCedula.get())
        if cliente is not None:
            self.Correcto()
            self.btnBuscar.config(state="disabled")
            self.txtNombre.config(state="normal")
            self.txtNombre.delete(0, "end")
            self.txtNombre.insert(0, cliente.nombre)
            self.txtNombre.config(state="disabled")
            self.txtApellido.config(state="normal")
            self.txtApellido.delete(0, "end")
            self.txtApellido.insert(0, cliente.apellido)
            self.txtApellido.config(state="disabled")
            self.txtTelefono.config(state="normal")
            self.txtTelefono.delete(0, "end")
            self.txtTelefono.insert(0, cliente.telefono)
            self.txtTelefono.config(state="disabled")
            self.txtEmail.config(state="normal")
            self.txtEmail.delete(0, "end")
            self.txtEmail.insert(0, cliente.email)
            self.txtEmail.config(state="disabled")
            self.btnEliminar.config(state="normal")
            
        else:
            messagebox.showinfo("Advertencia", "El número de cédula no se encontró")
            self.Limpiar()

    def Limpiar(self, event=None):
        """
        Limpia todos los campos de entrada y deshabilita los botones relevantes.

        Args:
            event (Event, optional): Evento que desencadena la función. Defaults to None.
        """
        self.Limpiar_Sonido()
        self.txtCedula.delete(0, END)
        self.txtCedula.configure(background='white')
        self.txtNombre.config(state='normal')
        self.txtNombre.delete(0, END)
        self.txtApellido.config(state='normal')
        self.txtApellido.delete(0, END)
        self.txtTelefono.config(state='normal')
        self.txtTelefono.delete(0, END)
        self.txtEmail.config(state='normal')
        self.txtEmail.delete(0, END)
        self.btnEliminar.config(state="disabled")
        self.btnBuscar.config(state="disabled")

    def mostrarAyuda(self, event):
        """
        Muestra un mensaje de ayuda al usuario y reproduce un sonido de ayuda.

        Args:
            event (Event): Evento que desencadena la función.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe introducir el número de cédula y luego presionar el botón buscar, posteriormente presionar el botón eliminar.")

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
        Reproduce un sonido de limpiar utilizando Pygame en un hilo separado.

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
        self.ventana.title("Eliminar cliente")
        self.ventana.config(width=300, height=300)
        self.corresponsal = corresponsal

        self.lblTitulo = tk.Label(self.ventana, text="Eliminar Cliente")
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
        self.lblApellido = tk.Label(self.ventana, text="Apellidos:")
        self.lblApellido.place(relx= 0.1, rely=0.4)
        self.txtApellido = tk.Entry(self.ventana, width=25)
        self.txtApellido.place(relx= 0.3, rely=0.4, width= 150, height= 25)
        self.lblTelefono = tk.Label(self.ventana, text="Telefono:")
        self.lblTelefono.place(relx= 0.1, rely=0.5)
        self.txtTelefono = tk.Entry(self.ventana, width=25)
        self.txtTelefono.place(relx= 0.3, rely=0.5, width= 150, height= 25)
        self.lblEmail = tk.Label(self.ventana, text="Email:")
        self.lblEmail.place(relx= 0.1, rely=0.6)
        self.txtEmail = tk.Entry(self.ventana, width=25)
        self.txtEmail.place(relx= 0.3, rely=0.6, width= 150, height= 25)

        iconoEliminar = Image.open(r"iconos\eliminar.png")
        iconoEliminar = iconoEliminar.resize((20, 20))
        self.iconoEliminar = ImageTk.PhotoImage(iconoEliminar)
        self.btnEliminar = tk.Button(self.ventana, image=self.iconoEliminar, text="Eliminar", state="disabled", compound="left", command=lambda: self.eliminarCliente())
        self.btnEliminar.place(relx= 0.5, rely=0.8, anchor="center")
        Tooltip(self.btnEliminar, "Presione para eliminar el Cliente!\nAlt+e")
        self.ventana.bind("<Alt-e>", self.eliminarCliente)

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