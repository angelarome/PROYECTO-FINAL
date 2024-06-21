import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from Controller.Corresponsal import Corresponsal
from PIL import Image, ImageTk
import pygame
import threading

class Loggin():
    
    def salirSistema(self, event=None): 
        """
        Muestra un mensaje de confirmación para salir del sistema y destruye la ventana si se confirma la salida.

        Args:
            event: Evento de disparo (por defecto None).
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "Esta seguro de Salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass
        
    def validarIngreso(self, event=None):
        """
        Intenta iniciar sesión con el nombre de usuario y contraseña proporcionados. 
        Muestra un mensaje de error si falla la autenticación.

        Args:
            event: Evento de disparo (por defecto None).
        """
        miUsuario = Corresponsal()
        try:
            miUsuario.iniciarSesion(self.txtUsuario.get(), self.txtPassword.get(), self.ventana)

        except Exception as e:
            self.Error()
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")

    def verCaracteres(self, event=None):
        """
        Muestra los caracteres de la contraseña en texto plano.

        Args:
            event: Evento de disparo (por defecto None).
        """
        self.Clave()
        self.txtPassword.configure(show='')
        self.btnVer.config(image=self.iconoOculto)

    def ocultarCaracteres(self, event):
        """
        Oculta los caracteres de la contraseña sustituyéndolos por asteriscos.

        Args:
            event: Evento de disparo.
        """
        self.Clave()
        self.txtPassword.configure(show='*')
        self.btnVer.config(image=self.iconoVer)

    def validarNombre(self, event):
        """
        Valida y gestiona la entrada del nombre del cliente.

        Args:
            event (tk.Event): Evento de teclado que desencadena la validación.
        """
        caracter = event.keysym
        if caracter.isalpha():
            self.txtUsuario.configure(background='#90EE90')
        else:
            self.txtUsuario.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtUsuario.delete(len(self.txtUsuario.get()) - 1, END)

    def validarLongitud(self, event):
        """
        Valida que la longitud de la contraseña sea de al menos 8 caracteres.

        Args:
            event: Evento de teclado.
        """
        caracter = event.keysym  
        if(caracter.isdigit()):  
            self.txtPassword.configure(background='#90EE90')
        else:
            self.txtPassword.configure(background='#FFCCCC')
            if(event.keysym != "BackSpace"): 
                self.txtPassword.delete(len(self.txtPassword.get())-1, END) 

        if(len(self.txtPassword.get()) >= 8): 
            self.btnIngresar.config(state="normal") 
    
    def mostrarAyuda(self, event):
        """
        Muestra un mensaje de ayuda con instrucciones para iniciar sesión.

        Args:
            event: Evento de disparo.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe diligenciar su nombre de usuario y la contraseña \n luego presione el botón ingresar.")
    
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
    
    def Error(self):
        """
        Reproduce un sonido de error.

        Utiliza threading para reproducir el sonido en un hilo separado.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\error (online-audio-converter.com).mp3')
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
    
    def Clave(self):
        """
        Reproduce un sonido relacionado con la contraseña.

        Utiliza threading para reproducir el sonido en un hilo separado.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\clave.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de Sesión")
        self.ventana.resizable(0,0)
        self.ventana.config(width=310, height=150)
        
        self.lblTitulo = tk.Label(self.ventana, text="Inicio Sesión")
        self.lblTitulo.place(relx=0.5, rely=0.05, anchor="center")
        self.lblUsuario = tk.Label(self.ventana, text="Usuario:")
        self.lblUsuario.place(relx=0.1, rely=0.15)
        self.txtUsuario = tk.Entry(self.ventana)
        self.txtUsuario.place(relx=0.35, rely=0.15)
        Tooltip(self.txtUsuario, "Ingrese su nombre y apellido")
        self.txtUsuario.bind("<KeyRelease>", self.validarNombre)
        self.lblPassword = tk.Label(self.ventana, text="Password:")
        self.lblPassword.place(relx=0.1, rely=0.37)
        self.txtPassword = tk.Entry(self.ventana, show="*")
        self.txtPassword.place(relx=0.35, rely=0.37)
        Tooltip(self.txtPassword, "Ingrese su número de cédula")

        iconoIngresar = Image.open(r"iconos\iniciar.png")
        iconoIngresar = iconoIngresar.resize((20, 20))
        self.iconoIngresar = ImageTk.PhotoImage(iconoIngresar)
        self.btnIngresar = tk.Button(self.ventana, image=self.iconoIngresar, text=" Ingresar",  compound="left", command=lambda: self.validarIngreso(), state="disabled")
        self.btnIngresar.place(relx=0.43, rely=0.67, anchor="center")
        Tooltip(self.btnIngresar, "Presione para ingresar al Sistema!\nAlt+e")
        self.ventana.bind("<Alt-e>", self.validarIngreso)   

        iconoSalir = Image.open(r"iconos\cerrar-sesion.png")
        iconoSalir = iconoSalir.resize((20, 20))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        self.btnSalir = tk.Button(self.ventana, image=self.iconoSalir, text=" Salir", compound="left", command=lambda: self.salirSistema())
        self.btnSalir.place(relx=0.60, rely=0.58)
        Tooltip(self.btnSalir, "Presione para salir del sistema!\nAlt+s")
        self.ventana.bind("<Alt-s>", self.salirSistema)   

        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.ventana, image= self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-30, y=10, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+l")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-l>', self.mostrarAyuda)

        iconoVer = Image.open(r"iconos\ver.png")
        iconoVer = iconoVer.resize((20, 20))
        self.iconoVer = ImageTk.PhotoImage(iconoVer)

        iconoOculto = Image.open(r"iconos\invisible.png")  
        iconoOculto = iconoOculto.resize((20, 20))
        self.iconoOculto = ImageTk.PhotoImage(iconoOculto)

        self.btnVer = tk.Button(self.ventana, image=self.iconoVer)
        self.btnVer.place(relx=0.78, rely=0.35, width=25, height=25)
        Tooltip(self.btnVer, "Presione para ver la contraseña!\nAlt+v")
        self.btnVer.bind("<Button-1>", self.verCaracteres)
        self.btnVer.bind("<ButtonRelease-1>", self.ocultarCaracteres)
        self.ventana.bind("<Alt-v>", self.verCaracteres)   

        self.txtPassword.bind("<KeyRelease>", self.validarLongitud)

        self.ventana.mainloop()

    