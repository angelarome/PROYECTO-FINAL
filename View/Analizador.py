import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import date
from Model.ConexionUsuario import ConexionUsuario


class Analizador:
    """
    Clase que proporciona métodos para analizar datos relacionados con las cuentas y fechas.
    Utiliza la clase ConexionUsuario para interactuar con la base de datos.
    """

    def SaldoPromedio(self):
        """
        Calcula el saldo promedio de todas las cuentas registradas.

        Returns:
            float: El saldo promedio de todas las cuentas.
                   Si no hay cuentas registradas o se produce un error, devuelve 0.0.
        """
        miConexion = ConexionUsuario()
        miConexion.crearConexion()
        con = miConexion.getConexion()
        cursor = con.cursor()

        try:
            cursor.execute("SELECT avg(saldo) FROM cuenta;")
            promedio_resultado = cursor.fetchone()[0]  
            if promedio_resultado is not None:
                promedio = float(promedio_resultado) 
            else:
                promedio = 0.0  

            return promedio

        except Exception as e:
            print(f"Error al obtener el promedio de saldo: {e}")
            return 0.0  

        finally:
            miConexion.cerrarConexion()

    def fechaActual(self):
        """
        Obtiene la fecha actual del sistema.

        Returns:
            datetime.date: Objeto de fecha que representa la fecha actual.
        """
        fecha_actual = date.today()
        return fecha_actual
