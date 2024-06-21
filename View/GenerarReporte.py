import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import date
from Model.ConexionUsuario import ConexionUsuario
from View.Analizador import Analizador
from tkinter import ttk
from Tooltip import Tooltip
from PIL import Image, ImageTk
import pygame
import threading

class GenerarReporte():
    def mostrarAyuda(self, event):
        """
        Muestra una ayuda al usuario y reproduce un sonido de ayuda.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Da click en el botón generar reporte")
    
    def salirSistema(self, event=None):
        """
        Solicita confirmación para salir del sistema y reproduce un sonido de pregunta.
        """
        self.Pregunta()
        respuesta = messagebox.askquestion("Confirmación", "¿Está seguro de salir?")
        if respuesta == "yes":
            self.ventana.destroy()
        else:
            pass

    def Reporte(self, event=None):
        """
        Genera un reporte de cuentas mostrando información parcial de cada cuenta.
        """
        try:
            miConexion = ConexionUsuario()
            miConexion.crearConexion()
            con = miConexion.getConexion()
            cursor = con.cursor()
            cursor.execute("SELECT numero_cuenta, cliente, saldo FROM cuenta")
            listaCuentas = cursor.fetchall()
            self.Correcto()
            self.btn_reporte.config(state="disabled")
            for cuenta in listaCuentas:
                numero_cuenta = str(cuenta[0])
                cedula_completa = cuenta[1]
                saldo = cuenta[2]
                if len(cedula_completa) >= 4:
                    cedula_mostrada = '*' * (len(cedula_completa) - 4) + cedula_completa[-4:]
                else:
                    cedula_mostrada = cedula_completa 
                if len(numero_cuenta) >= 4:
                    numero_cuenta_mostrada = '*' * (len(numero_cuenta) - 4) + numero_cuenta[-4:]
                else:
                    numero_cuenta_mostrada = numero_cuenta

                self.datos.insert("", "end", values=(numero_cuenta_mostrada, cedula_mostrada, saldo))

        except Exception as e:
            self.Error()
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")

    def TotalCuentas(self):
        """
        Obtiene el total de cuentas almacenadas en la base de datos.
        """
        miConexion = ConexionUsuario()
        miConexion.crearConexion()
        con = miConexion.getConexion()
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM cuenta")
        total_cuentas = cursor.fetchone()[0] 
        return total_cuentas
    
    def Promedio(self):
        """
        Calcula el saldo promedio de todas las cuentas.
        """
        total = Analizador()
        return total.SaldoPromedio()

    def fechaAnalizador(self):
        """
        Obtiene la fecha actual utilizando el analizador.
        """
        fecha = Analizador()
        return fecha.fechaActual()
    
    def fechaActual(self):
        """
        Obtiene la fecha actual del sistema.
        """
        fecha_actual = date.today()
        return fecha_actual

    def Error(self):
        """
        Reproduce un sonido de error.
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\error (online-audio-converter.com).mp3')
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

    def Pregunta(self):
        """
        Reproduce un sonido de pregunta.
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
        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\ayuda.mp3')
            pygame.mixer.music.play()
        
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def __init__(self, MenuCorresponsal):
        self.ventana = tk.Toplevel(MenuCorresponsal)
        self.ventana.title("Reporte de Cuentas")
        self.ventana.resizable(0, 0)

        self.frame = tk.Frame(self.ventana)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.datos = ttk.Treeview(self.frame, columns=("Numero Cuenta", "Cliente", "Saldo"), show="headings")
        self.datos.heading("Numero Cuenta", text="Número Cuenta")
        self.datos.heading("Cliente", text="Cliente")
        self.datos.heading("Saldo", text="Saldo")
        self.datos.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        iconoreporte = Image.open(r"iconos\reporte-de-negocios.png")
        iconoreporte = iconoreporte.resize((20, 20))
        self.iconoreporte = ImageTk.PhotoImage(iconoreporte)
        self.btn_reporte = tk.Button(self.frame, image=self.iconoreporte, text="Generar Reporte", compound="left", command=lambda: self.Reporte())
        self.btn_reporte.grid(row=1, column=0, pady=10)
        Tooltip(self.btn_reporte, "Presione para generar el reporte!\nAlt+r")
        self.ventana.bind("<Alt-r>", self.Reporte)  


        iconoSalir = Image.open(r"iconos\cerrar-sesion.png")
        iconoSalir = iconoSalir.resize((20, 20))
        self.iconoSalir = ImageTk.PhotoImage(iconoSalir)
        self.btnSalir = tk.Button(self.frame, image=self.iconoSalir, text=" Salir", compound="left", command=lambda: self.salirSistema())
        self.btnSalir.grid(row=2, column=0, pady=10)
        Tooltip(self.btnSalir, "Presione para salir del sistema!\nAlt+s")
        self.ventana.bind("<Alt-s>", self.salirSistema)  

        self.lbltotal = tk.Label(self.frame, text=f"Total de cuentas: {self.TotalCuentas()}")
        self.lbltotal.grid(row=1, column=1, pady=10)

        self.lblpromedio = tk.Label(self.frame, text=f"Promedio: {self.Promedio()}")
        self.lblpromedio.grid(row=2, column=1, pady=10)

        self.lblfecha = tk.Label(self.frame, text=f"Fecha del reporte: {self.fechaActual()}")
        self.lblfecha.grid(row=1, column=2, pady=10)

        self.lblfechaA = tk.Label(self.frame, text=f"Fecha del Analizador: {self.fechaAnalizador()}")
        self.lblfechaA.grid(row=2, column=2, pady=10)

        iconoAyuda = Image.open(r"iconos\signo-de-interrogacion.png")
        iconoAyuda = iconoAyuda.resize((20, 20))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =tk.Button(self.frame, image=self.iconoAyuda)
        self.btnAyuda.place(relx=1, x=-45, y=25, width=25, height=25)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+a")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-a>', self.mostrarAyuda)

        self.ventana.mainloop() 

        self.ventana.mainloop() 