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

class Deposito(Transaccion):
    """
    Clase para gestionar el proceso de depósito en el sistema de corresponsales.
    Hereda de la clase Transaccion.

    Attributes:
        Se heredan los atributos de la clase Transaccion:
            - numero_transaccion (str): Número de transacción asociado al depósito.
            - monto (str): Monto del depósito realizado.
            - cuenta (str): Número de cuenta asociado al depósito.
    """

    def __init__(self, numero_transaccion="", monto="", cuenta=""):
        """
        Inicializa una nueva instancia de Deposito.

        Args:
            numero_transaccion (str): Número de transacción asociado al depósito.
            monto (str): Monto del depósito realizado.
            cuenta (str): Número de cuenta asociado al depósito.
        """
        Transaccion.__init__(self, numero_transaccion, monto, cuenta)

    def mostrarAyuda(self, event):
        """
        Muestra un mensaje de ayuda al usuario y reproduce un sonido de ayuda al presionar un botón.

        Args:
            event: El evento asociado al botón de ayuda.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe introducir el número de cuenta y luego presionar el botón buscar, posteriormente poner el monto y dar click al botón depositar.")

    def Deposito(self, event=None):
        """
        Realiza el proceso de depósito en la cuenta ingresada, actualizando el saldo y registrando la transacción.

        Args:
            event: El evento asociado al botón de realizar depósito.
        """
        if self.corresponsal:
            self.corresponsal.Deposito(self.txtTransaccion.get(), self.txtMonto.get(), self.txtNumeroCuenta.get())
            self.Limpiar()
        else:
            try:
                monto = self.txtMonto.get()
                monto = float(monto)
            except ValueError:
                self.Error()
                messagebox.showerror("Error", "El monto ingresado no es válido.")
                return
            
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
                    nuevo_saldo = saldo_actual + monto
                    
                    self.Pregunta()
                    respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea depositar ${monto}?")

                    if respuesta == "yes":
                        cursor.execute("UPDATE cuenta SET saldo = ? WHERE numero_cuenta = ?", (nuevo_saldo, numero_cuenta))
                        con.commit()
                        cursor.execute("INSERT INTO transaccion(numero_transaccion, tipo, monto, cuenta) VALUES (?, 'Deposito', ?, ?)", (numero_transaccion, monto, numero_cuenta))
                        con.commit()
                        self.Correcto()
                        messagebox.showinfo("Éxito", f"Se ha realizado el depósito de ${monto}. Nuevo saldo: ${nuevo_saldo}")
                        self.txtTransaccion.config(state="normal")
                        self.txtTransaccion.delete(0, "end")
                        self.txtTransaccion.insert(0, self.Numero_transaccion())
                        self.txtTransaccion.config(state="disabled")
                        self.Limpiar()
                    else:
                        self.Error()
                        messagebox.showinfo("Cancelación", "Operación de depósito cancelada")

            except Exception as e:
                self.Error()
                messagebox.showerror("Error", f"Error al realizar el depósito: {str(e)}")
            finally:
                miConexion.cerrarConexion()

    def validarMonto(self, event):
        """
        Valida que solo se ingresen números válidos en el campo de monto del depósito.

        Args:
            event: El evento asociado a la entrada en el campo de monto.
        """
        caracter = event.keysym  
        if caracter.isdigit():  
            self.txtMonto.configure(background='#90EE90')
        else:
            self.txtMonto.configure(background='#FFCCCC')
            if(event.keysym != "BackSpace"): 
                self.txtMonto.delete(len(self.txtMonto.get())-1, END) 
        
        if(len(self.txtNumeroCuenta.get()) >= 8 and len(self.txtMonto.get()) >= 3):
            self.btnDepositar.config(state="normal") 
        else:
            self.btnDepositar.config(state="disabled")  

    def validarNumeroCuenta(self, event):
        """
        Valida que solo se ingresen números válidos en el campo de número de cuenta.

        Args:
            event: El evento asociado a la entrada en el campo de número de cuenta.
        """
        caracter = event.keysym  
        if caracter.isdigit():  
            self.txtNumeroCuenta.configure(background='#90EE90')
        else:
            self.txtNumeroCuenta.configure(background='#FFCCCC')
            if(event.keysym != "BackSpace"): 
                self.txtNumeroCuenta.delete(len(self.txtNumeroCuenta.get())-1, END) 
        
        if(len(self.txtNumeroCuenta.get()) >= 8 ):
            self.btnBuscar.config(state="normal") 
        else:
            self.btnBuscar.config(state="disabled")  

    def buscarCuenta(self, event=None):
        """
        Busca una cuenta asociada al número de cuenta ingresado y muestra la información del cliente.

        Args:
            event: El evento asociado al botón de buscar cuenta.
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
        Genera un número de transacción único para el depósito.

        Returns:
            int: Número de transacción único generado.
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

            except sqlite3.IntegrityError as e:
                continue

            finally:
                miConexion.cerrarConexion()

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
        else:
            pass
            
    def Limpiar(self, event=None):
        """
        Limpia los campos de entrada y restablece los estados de los botones.

        Args:
            event: El evento asociado al botón de limpiar campos.
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
            self.btnDepositar.config(state="disabled")

        else:
            self.Limpiar_Sonido()
            self.txtMonto.config(state='normal')
            self.txtMonto.delete(0, END)
            self.txtMonto.configure(background='white')


    def Error(self):
        """
        Reproduce un sonido de error al detectar un error en la operación.

        El sonido de error se reproduce en un hilo separado para evitar bloqueos
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\error (online-audio-converter.com).mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Correcto(self):
        """
        Reproduce un sonido de éxito al realizar una operación exitosa.

        El sonido de correcto se reproduce en un hilo separado para evitar bloqueos.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\correcto.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Pregunta(self):
        """
        Reproduce un sonido de pregunta al realizar una pregunta al usuario.

        El sonido de pregunta se reproduce en un hilo separado para evitar bloqueos.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Ayuda(self):
        """
        Reproduce un sonido de ayuda al mostrar un mensaje de ayuda al usuario.

        El sonido de ayuda se reproduce en un hilo separado para evitar bloqueos.

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

        El sonido de limpieza se reproduce en un hilo separado para evitar bloqueos.
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
        self.ventana.title("Realizar deposito")
        self.ventana.config(width=350, height=280)
        self.corresponsal = corresponsal
        self.cuenta = cuenta

        self.lblTitulo = tk.Label(self.ventana, text="Realizar deposito")
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
        Tooltip(self.txtMonto, "Ingrese el monto a depositar")
        self.txtMonto.bind("<KeyRelease>", self.validarMonto)
        self.lblCedula = tk.Label(self.ventana, text="Cédula:")
        self.lblCedula.place(relx= 0.1, rely=0.65)
        self.txtCedula = tk.Entry(self.ventana, width=25)
        self.txtCedula.place(relx= 0.37, rely=0.65, width= 150, height= 25)

        iconoDepositar = Image.open(r"iconos\flecha.png")
        iconoDepositar = iconoDepositar.resize((20, 20))
        self.iconoDepositar = ImageTk.PhotoImage(iconoDepositar)
        self.btnDepositar = tk.Button(self.ventana, image=self.iconoDepositar, text=" Depositar", state="disabled", compound="left", command=lambda: self.Deposito())
        self.btnDepositar.place(relx= 0.5, rely=0.85, anchor="center")
        Tooltip(self.btnDepositar, "Presione para Depositar!\nAlt+d")
        self.ventana.bind("<Alt-d>", self.Deposito)

        iconoSalir = Image.open(r"iconos\cerrar-sesion.png")
        iconoSalir = iconoSalir.resize((20, 20))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        self.btnSalir = tk.Button(self.ventana, image=self.iconoSalir, text=" Salir", compound="left", command=lambda: self.salirSistema())
        self.btnSalir.place(relx=0.8, rely=0.85, anchor="center")
        Tooltip(self.btnSalir, "Presione para salir del sistema!\nAlt+s")
        self.ventana.bind("<Alt-s>", self.salirSistema)  
        
        iconoLimpiar = Image.open(r"iconos\borrar.png")
        iconoLimpiar = iconoLimpiar.resize((20, 20))
        self.iconoLimpiar = ImageTk.PhotoImage(iconoLimpiar)
        self.btnLimpiar = tk.Button(self.ventana, image=self.iconoLimpiar, text=" Limpiar", compound="left", command=lambda:self.Limpiar())
        self.btnLimpiar.place(relx= 0.2, rely=0.85, anchor="center")
        Tooltip(self.btnLimpiar, "Presione para limpiar los campos!\nAlt+l")
        self.ventana.bind("<Alt-l>", self.Limpiar)  

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