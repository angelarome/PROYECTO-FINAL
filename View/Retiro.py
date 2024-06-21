import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Tooltip import Tooltip
from Controller.Transaccion import Transaccion
from Model.ConexionUsuario import ConexionUsuario
from PIL import Image, ImageTk
import sqlite3
import pygame
import threading


class Retiro(Transaccion):
    """
    Clase para gestionar la transacción de retiro en el sistema.

    Attributes:
        numero_transaccion (str): Número de transacción (opcional).
        monto (str): Monto del retiro (opcional).
        cuenta (str): Número de cuenta asociada al retiro (opcional).
    """

    def __init__(self, numero_transaccion="", monto="", cuenta=""):
        """
        Constructor de la clase Retiro que inicializa los atributos de la clase base Transaccion.

        Args:
            numero_transaccion (str): Número de transacción (opcional).
            monto (str): Monto del retiro (opcional).
            cuenta (str): Número de cuenta asociada al retiro (opcional).
        """
        Transaccion.__init__(self, numero_transaccion, monto, cuenta)

    def salirSistema(self, event=None):
        """
        Muestra una pregunta de confirmación y cierra la ventana si el usuario confirma.

        Args:
            event: Evento asociado al método (opcional).
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "¿Está seguro de Salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass

    def Retirar(self, event=None):
        """
        Realiza la operación de retiro según los datos ingresados por el usuario.

        Args:
            event: Evento asociado al método (opcional).
        """
        if self.corresponsal:
            self.corresponsal.Retiro(self.txtTransaccion.get(), self.txtMonto.get(), numero_cuenta=self.txtNumeroCuenta.get())
            self.Limpiar()
        else:
            try:
                monto = self.txtMonto.get()
                monto = float(monto)
            except ValueError:
                self.Error()
                messagebox.showerror("Error", "El monto ingresado no es válido.")
            
            try:
                miConexion = ConexionUsuario()
                miConexion.crearConexion()
                con = miConexion.getConexion()
                cursor = con.cursor()
                numero_cuenta = self.txtNumeroCuenta.get()
                numero_transaccion = self.txtTransaccion.get()
                cursor.execute("SELECT saldo FROM cuenta WHERE numero_cuenta = ?", (numero_cuenta,))
                saldo_resultado = cursor.fetchone()

                if saldo_resultado:
                    saldo_actual = saldo_resultado[0]  
                    if saldo_actual >= monto:
                        nuevo_saldo = saldo_actual - monto
                        self.Pregunta()
                        respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea retirar ${monto}.")
                        if respuesta == "yes":
                            cursor.execute("UPDATE cuenta SET saldo = ? WHERE numero_cuenta = ?", (nuevo_saldo, numero_cuenta))
                            con.commit()
                            cursor.execute("INSERT INTO transaccion(numero_transaccion, tipo, monto, cuenta) VALUES (?, 'Retiro', ?, ?)", (numero_transaccion, monto, numero_cuenta))
                            con.commit()
                            self.Correcto()
                            messagebox.showinfo("Éxito", f"Se ha realizado el retiro de ${monto}. Nuevo saldo: ${nuevo_saldo}")
                            self.txtTransaccion.config(state="normal")
                            self.txtTransaccion.delete(0, "end")
                            self.txtTransaccion.insert(0, self.Numero_transaccion())
                            self.txtTransaccion.config(state="disabled")
                            self.Limpiar()
                        else:
                            self.Error()
                            messagebox.showinfo("Cancelación", "Operación de eliminación cancelada")
                    else:
                        self.Error()
                        messagebox.showwarning("Advertencia", "El monto que desea retirar es mayor a su saldo actual")

            except Exception as e:
                self.Error()
                messagebox.showerror("Error", f"Error al realizar el retiro: {str(e)}")
            miConexion.cerrarConexion()

    def validarMonto(self, event):
        """
        Valida la entrada de caracteres en el campo de monto y habilita el botón de retiro cuando se cumple la longitud mínima.

        Args:
            event: Evento de teclado asociado al método.
        """
        caracter = event.keysym  
        if caracter.isdigit():  
            self.txtMonto.configure(background='#90EE90')
        else:
            self.txtMonto.configure(background='#FFCCCC')
            if event.keysym != "BackSpace": 
                self.txtMonto.delete(len(self.txtMonto.get())-1, END) 
        if (len(self.txtNumeroCuenta.get()) >= 8 and len(self.txtMonto.get()) >= 3):
            self.btnRetirar.config(state="normal") 
        else:
            self.btnRetirar.config(state="disabled")  

    def validarNumeroCuenta(self, event):
        """
        Valida la entrada de caracteres en el campo de número de cuenta y habilita el botón de búsqueda cuando se cumple la longitud mínima.

        Args:
            event: Evento de teclado asociado al método.
        """
        caracter = event.keysym  
        if caracter.isdigit():  
            self.txtNumeroCuenta.configure(background='#90EE90')
        else:
            self.txtNumeroCuenta.configure(background='#FFCCCC')
            if event.keysym != "BackSpace": 
                self.txtNumeroCuenta.delete(len(self.txtNumeroCuenta.get())-1, END) 
        if len(self.txtNumeroCuenta.get()) >= 8:
            self.btnBuscar.config(state="normal") 
        else:
            self.btnBuscar.config(state="disabled")  

    def buscarCuenta(self, event=None):
        """
        Busca una cuenta por su número y muestra los datos asociados en los campos correspondientes.

        Args:
            event: Evento asociado al método (opcional).
        """
        cuenta = self.corresponsal.buscarCuenta(self.txtNumeroCuenta.get())
        if cuenta is not None:
            self.Correcto()
            self.txtTransaccion.config(state="normal")
            self.txtTransaccion.delete(0, "end")
            self.txtTransaccion.insert(0, self.Numero_transaccion())
            self.txtTransaccion.config(state="disabled")
            self.txtCedula.config(state="normal")
            self.txtCedula.delete(0, "end")
            self.txtCedula.insert(0, cuenta.cliente)
            self.txtCedula.config(state="disabled")
            self.btnBuscar.config(state="disabled")
        else:
            self.Limpiar()
            

    def Numero_transaccion(self):
        """
        Genera un nuevo número de transacción para la operación de retiro.

        Returns:
            int: Nuevo número de transacción generado.
        """
        miConexion = ConexionUsuario()
        miConexion.crearConexion()
        con = miConexion.getConexion()
        cursor = con.cursor()
        while True:
            try:
                cursor.execute("SELECT MAX(numero_transaccion) FROM transaccion")
                resultado = cursor.fetchone()

                if resultado and resultado[0] is not None:
                    numero_transaccion = int(resultado[0]) + 1
                else:
                    numero_transaccion = 1  

                return numero_transaccion

            except sqlite3.IntegrityError:
                continue

            finally:
                miConexion.cerrarConexion()



    def Limpiar(self, event=None):
        """
        Limpia los campos de entrada y restablece los estados y configuraciones iniciales según el tipo de operación.

        Args:
            event: Evento asociado al método (opcional).
        """
        if self.corresponsal:
            self.Limpiar_Sonido()
            self.txtCedula.config(state='normal')
            self.txtCedula.delete(0, END)
            self.txtNumeroCuenta.config(state='normal')
            self.txtNumeroCuenta.delete(0, END)
            self.txtNumeroCuenta.configure(background='white')
            self.txtMonto.config(state='normal')
            self.txtMonto.delete(0, END)
            self.txtMonto.configure(background='white')
            self.txtTransaccion.config(state='normal')
            self.txtTransaccion.delete(0, END)
            self.btnBuscar.config(state="disabled")
            self.btnRetirar.config(state="disabled")

        else:
            self.Limpiar_Sonido()
            self.txtMonto.config(state='normal')
            self.txtMonto.delete(0, END)
            self.txtMonto.configure(background='white')


    def mostrarAyuda(self, event):
        """
        Muestra una ventana de ayuda y reproduce un sonido de ayuda.

        Args:
            event: Evento asociado al método.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe introducir el número de cuenta y luego presionar el botón buscar, posteriormente poner el monto y dar click al botón retirar ")

    def Error(self):
        """
        Reproduce un sonido de error utilizando threading para evitar bloqueos.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\error (online-audio-converter.com).mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Correcto(self):
        """
        Reproduce un sonido de éxito utilizando threading para evitar bloqueos.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\correcto.mp3')
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


    def __init__(self, menu, corresponsal, cuenta=None, cliente=None):
        self.ventana = tk.Toplevel(menu)
        self.ventana.resizable(0,0)
        self.ventana.title("Realizar retiro")
        self.ventana.config(width=350, height=280)
        self.corresponsal = corresponsal
        self.cuenta = cuenta

        self.lblTitulo = tk.Label(self.ventana, text="Realizar retiro")
        self.lblTitulo.place(relx= 0.5, rely=0.1, anchor="center")
        
        self.lblNumeroCuenta = tk.Label(self.ventana, text="Numero de Cta:")
        self.lblNumeroCuenta.place(relx= 0.1, rely=0.2)
        self.txtNumeroCuenta = tk.Entry(self.ventana, width=25)
        self.txtNumeroCuenta.place(relx= 0.37, rely=0.2, width= 150, height= 25)
        self.txtNumeroCuenta.bind("<KeyRelease>", self.validarNumeroCuenta)
        self.lblTransaccion = tk.Label(self.ventana, text="Transacción No:")
        self.lblTransaccion.place(relx= 0.1, rely=0.35)
        self.txtTransaccion = tk.Entry(self.ventana, width=25)
        self.txtTransaccion.place(relx= 0.37, rely=0.35, width= 150, height= 25)
        self.lblMonto = tk.Label(self.ventana, text="Monto:")
        self.lblMonto.place(relx= 0.1, rely=0.50)
        self.txtMonto = tk.Entry(self.ventana, width=25)
        self.txtMonto.place(relx= 0.37, rely=0.50, width= 150, height= 25)
        Tooltip(self.txtMonto, "Ingrese el monto a retirar")
        self.txtMonto.bind("<KeyRelease>", self.validarMonto)
        self.lblCedula = tk.Label(self.ventana, text="Cédula:")
        self.lblCedula.place(relx= 0.1, rely=0.65)
        self.txtCedula = tk.Entry(self.ventana, width=25)
        self.txtCedula.place(relx= 0.37, rely=0.65, width= 150, height= 25)

        iconoRetirar = Image.open(r"iconos\cajero-automatico.png")
        iconoRetirar = iconoRetirar.resize((20, 20))
        self.iconoRetirar = ImageTk.PhotoImage(iconoRetirar)
        self.btnRetirar = tk.Button(self.ventana, image=self.iconoRetirar, text=" Retiro", compound="left", state="disabled", command=lambda: self.Retirar())
        self.btnRetirar.place(relx= 0.5, rely=0.85, anchor="center")
        Tooltip(self.btnRetirar, "Presione para retirar!\nAlt+r")
        self.ventana.bind('<Alt-r>', self.Retirar)

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
        self.btnSalir.place(relx=0.8, rely=0.85, anchor="center")
        Tooltip(self.btnSalir, "Presione para salir del sistema!\nAlt+s")
        self.ventana.bind("<Alt-s>", self.salirSistema)   

        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.ventana, image=self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-25, y=20, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+a")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-a>', self.mostrarAyuda)
        
        if self.corresponsal:
            iconoBuscar = Image.open(r"iconos\encontrar.png")
            iconoBuscar = iconoBuscar.resize((15, 15))
            self.iconoBuscar = ImageTk.PhotoImage(iconoBuscar)
            self.btnBuscar = tk.Button(self.ventana, image=self.iconoBuscar, text=" Buscar", compound="left", state="disabled", command=self.buscarCuenta)
            self.btnBuscar.place(relx=0.82, rely=0.2)
            Tooltip(self.btnBuscar, "Presione para buscar el número de cuenta!\nAlt+b")
            self.btnBuscar.bind('<Button-1>', self.buscarCuenta)
            self.ventana.bind('<Alt-b>', self.buscarCuenta)
            Tooltip(self.txtNumeroCuenta, "Ingrese el número de cuenta del cliente")

        else:
            self.txtNumeroCuenta.delete(0, "end")
            self.txtNumeroCuenta.insert(0, cuenta.numero_cuenta)
            self.txtNumeroCuenta.config(state="disabled")
            self.txtTransaccion.config(state="normal")
            self.txtTransaccion.delete(0, "end")
            self.txtTransaccion.insert(0, self.Numero_transaccion())
            self.txtTransaccion.config(state="disabled")
            self.txtCedula.config(state="normal")
            self.txtCedula.delete(0, "end")
            self.txtCedula.insert(0, cliente.cedula)
            self.txtCedula.config(state="disabled")
            
        self.ventana.mainloop()