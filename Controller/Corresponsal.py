from Model.ConexionUsuario import ConexionUsuario
from tkinter import messagebox
from View.MenuCajero import MenuCajero
from Controller.Usuario import Usuario
from Controller.Cliente import Cliente
from Controller.Cuenta import Cuenta
from View.MenuCliente import MenuCliente
import pygame
import threading

class Corresponsal(Usuario):
    def __init__(self, nombre_corresponsal="", direccion="", cedula="", nombre="", apellido="", telefono="", email=""):
        """
        Constructor de la clase Corresponsal.
        
        Args:
        - nombre_corresponsal (str): Nombre del corresponsal.
        - direccion (str): Dirección del corresponsal.
        - cedula (str): Cédula del corresponsal.
        - nombre (str): Nombre del usuario (heredado de la clase base Usuario).
        - apellido (str): Apellido del usuario (heredado de la clase base Usuario).
        - telefono (str): Teléfono del usuario (heredado de la clase base Usuario).
        - email (str): Correo electrónico del usuario (heredado de la clase base Usuario).
        """
        # Llama al constructor de la clase base Usuario
        Usuario.__init__(self, cedula, nombre, apellido, telefono, email)
        
        # Atributos específicos de Corresponsal
        self.nombre_corresponsal = nombre_corresponsal
        self.direccion = direccion
        
        # Atributos heredados de Usuario
        self.__cedula = cedula
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email
        
    # Métodos getter para obtener los atributos específicos de Corresponsal
    def getNombre_corresponsal(self):
        """Devuelve el nombre del corresponsal."""
        return self.nombre_corresponsal
    
    def getDireccion(self):
        """Devuelve la dirección del corresponsal."""
        return self.direccion
    
    # Métodos getter para obtener los atributos heredados de Usuario
    def getCedula(self):
        """Devuelve la cédula del usuario."""
        return self.__cedula
    
    def getNombre(self):
        """Devuelve el nombre del usuario."""
        return self.__nombre
    
    def getApellido(self):
        """Devuelve el apellido del usuario."""
        return self.__apellido
    
    def getTelefono(self):
        """Devuelve el teléfono del usuario."""
        return self.__telefono
    
    def getEmail(self):
        """Devuelve el correo electrónico del usuario."""
        return self.__email
    
    # Métodos setter para establecer los atributos específicos de Corresponsal
    def setNombre_corresponsal(self, nombre_corresponsal):
        """
        Establece el nombre del corresponsal.
        
        Args:
        - nombre_corresponsal (str): Nuevo nombre del corresponsal.
        """
        self.nombre_corresponsal = nombre_corresponsal
    
    def setDireccion(self, direccion):
        """
        Establece la dirección del corresponsal.
        
        Args:
        - direccion (str): Nueva dirección del corresponsal.
        """
        self.direccion = direccion
    
    # Métodos setter para establecer los atributos heredados de Usuario
    def setCedula(self, cedula):
        """
        Establece la cédula del usuario.
        
        Args:
        - cedula (str): Nueva cédula del usuario.
        """
        self.__cedula = cedula
    
    def setNombre(self, nombre):
        """
        Establece el nombre del usuario.
        
        Args:
        - nombre (str): Nuevo nombre del usuario.
        """
        self.__nombre = nombre
    
    def setApellido(self, apellido):
        """
        Establece el apellido del usuario.
        
        Args:
        - apellido (str): Nuevo apellido del usuario.
        """
        self.__apellido = apellido
    
    def setTelefono(self, telefono):
        """
        Establece el teléfono del usuario.
        
        Args:
        - telefono (str): Nuevo teléfono del usuario.
        """
        self.__telefono = telefono
    
    def setEmail(self, email):
        """
        Establece el correo electrónico del usuario.
        
        Args:
        - email (str): Nueva dirección de correo electrónico del usuario.
        """
        self.__email = email

    def iniciarSesion(self, nombreUsuario, password, loggin):
        """
        Método para iniciar sesión como corresponsal o cliente.
        
        Args:
        - nombreUsuario (str): Nombre de usuario para la sesión.
        - password (str): Contraseña del usuario para la sesión.
        - loggin: Objeto de inicio de sesión (no definido en el código proporcionado).
        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL
        
        # Busca si el usuario es corresponsal
        cursor.execute("SELECT usuario.cedula, usuario.nombre, usuario.apellido, corresponsal.nombre_corresponsal FROM usuario JOIN corresponsal ON corresponsal.usuario = usuario.cedula WHERE usuario.cedula = ? AND CONCAT(usuario.nombre, ' ', usuario.apellido) = ?", (password, nombreUsuario))
        listaCorresponsal = cursor.fetchall()
        
        if listaCorresponsal:
            corresponsal = listaCorresponsal[0]
            userName = corresponsal[1] + " " + corresponsal[2]
            if userName == nombreUsuario and corresponsal[0] == password:
                self.Inicio()
                messagebox.showinfo("Mensaje", f"Bienvenido corresponsal {nombreUsuario}")
                miCajero = Corresponsal(corresponsal[0], corresponsal[1], corresponsal[2], corresponsal[3])
                miMenu = MenuCajero(loggin, miCajero)
        
        # Si no es corresponsal, busca si el usuario en cliente
        else:
            cursor.execute("SELECT usuario.cedula, usuario.nombre, usuario.apellido FROM usuario JOIN cliente ON cliente.usuario = usuario.cedula WHERE usuario.cedula = ? AND CONCAT(usuario.nombre, ' ', usuario.apellido) = ?", (password, nombreUsuario))
            listaCliente = cursor.fetchall()
            
            if listaCliente:
                cursor.execute("SELECT cliente.usuario, usuario.nombre, usuario.apellido, cuenta.numero_cuenta FROM cuenta JOIN cliente ON cuenta.cliente = cliente.usuario JOIN usuario ON cliente.usuario = usuario.cedula WHERE cliente.usuario = ?", (password,))
                listaCuenta = cursor.fetchall()
                if listaCuenta:
                    cuenta = listaCuenta[0]
                    userName = cuenta[1] + " " + cuenta[2]
                    if userName == nombreUsuario and cuenta[0] == password:
                        self.Inicio()
                        messagebox.showinfo("Mensaje", f"Bienvenido cliente {nombreUsuario}")
                        miCliente = Cliente(cuenta[0], cuenta[1], cuenta[2])
                        miCuenta = Cuenta(numero_cuenta=cuenta[3])
                        corresponsal = None
                        miMenu = MenuCliente(loggin, corresponsal, miCuenta, miCliente)
    
                else:
                    self.Error()
                    messagebox.showwarning("Advertencia", "El nombre de usuario y/o contraseña no coinciden.")
            else:
                self.Error()
                messagebox.showwarning("Advertencia", "El nombre de usuario y/o contraseña no existe, verifique e intente nuevamente!")
        
        miConexion.cerrarConexion()
    
    def ingresarCliente(self, cedulaCliente, nombreCliente, apellidoCliente, telefonoCliente, correoCliente):
        """
        Método para ingresar un nuevo cliente en la base de datos.
        
        Args:
        - cedulaCliente (str): Cédula del nuevo cliente.
        - nombreCliente (str): Nombre del nuevo cliente.
        - apellidoCliente (str): Apellido del nuevo cliente.
        - telefonoCliente (str): Teléfono del nuevo cliente.
        - correoCliente (str): Correo electrónico del nuevo cliente.
        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL
        
        try:
            self.Pregunta()
            respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea crear al cliente con cédula {cedulaCliente}?")
            if respuesta == "yes":
                # Inserta los datos obtenidos en la tabla usuario y en la tabla cliente
                cursor.execute("INSERT INTO usuario(cedula, nombre, apellido, telefono, correo_electronico) VALUES (?, ?, ?, ?, ?)", (cedulaCliente, nombreCliente, apellidoCliente, telefonoCliente, correoCliente))
                con.commit()
                cursor.execute("INSERT INTO cliente(usuario) VALUES (?)", (cedulaCliente,))
                con.commit()
                self.Correcto()
                messagebox.showinfo("Éxito", f"El nuevo cliente con cédula {cedulaCliente} se registró correctamente")
            else:
                self.Error()
                messagebox.showinfo("Cancelación", "Operación de creación cancelada")
        except Exception as e:
             # En caso de error, se revierte cualquier cambio no confirmado en la base de datos
            con.rollback() 
            self.Error()
            messagebox.showerror("Error", f"Error al crear el cliente: {str(e)}")
        miConexion.cerrarConexion()


    def modificarCliente(self, cedulaCliente, nombreCliente, apellidoCliente, telefonoCliente, correoCliente):
        """
        Modifica los datos de un cliente en la base de datos.

        Args:
        - cedulaCliente (str): Cédula del cliente a modificar.
        - nombreCliente (str): Nuevo nombre del cliente.
        - apellidoCliente (str): Nuevo apellido del cliente.
        - telefonoCliente (str): Nuevo número de teléfono del cliente.
        - correoCliente (str): Nuevo correo electrónico del cliente.
        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        try:
            self.Pregunta()
            respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea modificar al cliente con cédula {cedulaCliente}?")
            if respuesta == "yes":
                # Ejecuta la actualización en la base de datos
                cursor.execute("UPDATE cliente JOIN usuario ON cliente.usuario = usuario.cedula SET usuario.nombre = %s, usuario.apellido = %s, usuario.telefono = %s, usuario.correo_electronico = %s WHERE usuario.cedula = %s", (nombreCliente, apellidoCliente, telefonoCliente, correoCliente, cedulaCliente))
                con.commit()
                self.Correcto()
                messagebox.showinfo("Éxito", f"Se ha modificado el cliente con cédula {cedulaCliente} con éxito")
            else:
                self.Error()
                messagebox.showinfo("Cancelación", "Operación de modificación cancelada")
        except Exception as e:
            con.rollback()
            self.Error()
            messagebox.showerror("Error", f"Error al modificar el cliente: {str(e)}")
        finally:
            miConexion.cerrarConexion()


    def eliminarCliente(self, cedulaCliente):
        """
        Elimina un cliente de la base de datos junto con su información asociada.

        Args:
        - cedulaCliente (str): Cédula del cliente que se desea eliminar.
        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        try:
            self.Pregunta()
            respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea eliminar al cliente con cédula {cedulaCliente}?")
            if respuesta == "yes":
                # Desactiva temporalmente la verificación de claves foráneas para evitar errores de integridad
                cursor.execute("SET foreign_key_checks = 0;")
                con.commit()

                # Elimina al cliente de las tablas 'cliente' y 'usuario'
                cursor.execute("DELETE from cuenta WHERE cliente = ?", (cedulaCliente,))
                con.commit()
                cursor.execute("DELETE FROM cliente WHERE usuario = ?", (cedulaCliente,))
                con.commit()
                cursor.execute("DELETE FROM usuario WHERE cedula = ?", (cedulaCliente,))
                con.commit()
                

                self.Correcto()
                messagebox.showinfo("Éxito", f"Se ha eliminado el cliente con cédula {cedulaCliente} con éxito")
            else:
                self.Error()
                messagebox.showinfo("Cancelación", "Operación de eliminación cancelada")
        except Exception as e:
             # En caso de error, se revierte cualquier cambio no confirmado en la base de datos
            con.rollback()
            self.Error()
            messagebox.showerror("Error", f"Error al eliminar el cliente: {str(e)}")
        finally:
            # Restablece la verificación de claves foráneas y cierra la conexión
            cursor.execute("SET foreign_key_checks = 1;")
            con.commit()
            miConexion.cerrarConexion()

    def buscarCliente(self, cedulaCliente):
        """
        Busca un cliente en la base de datos por su número de cédula.

        Args:
        - cedulaCliente (str): Número de cédula del cliente que se desea buscar.

        Returns:
        - Cliente: Objeto Cliente con la información del cliente encontrado, o None si no se encuentra.
        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        try:
            # Busca si en cliente el nùmero de cèdula
            cursor.execute("SELECT usuario FROM cliente WHERE usuario = ?", (cedulaCliente,))
            resultado = cursor.fetchone()

            if resultado:
                # Si encuentra el nùmero de cedula manda los datos obtenidos
                cursor.execute("SELECT usuario.cedula, usuario.nombre, usuario.apellido, usuario.telefono, usuario.correo_electronico FROM usuario LEFT JOIN cliente ON cliente.usuario = usuario.cedula WHERE usuario.cedula = ?", (cedulaCliente,))
                listaClientes = cursor.fetchall()

                if len(listaClientes) > 0:
                    cliente = listaClientes[0]
                    cliente2 = Cliente(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4])
                    self.Correcto()
                    return cliente2
                else:
                    messagebox.showwarning("Advertencia", f"No se ha encontrado un cliente con cédula {cedulaCliente}")
                    return None
            else: 
                return None

        except Exception as e:
            self.Error()
            messagebox.showerror("Error", f"Error al buscar cliente: {str(e)}")
        finally:
            miConexion.cerrarConexion()
    
    def ingresarCuenta(self, cedulaCliente, numero_cuenta, saldo):
        """
        Registra una nueva cuenta para un cliente en la base de datos.

        Args:
        - cedulaCliente (str): Número de cédula del cliente al que se asociará la cuenta.
        - numero_cuenta (str): Número de cuenta que se desea registrar.
        - saldo (float): Saldo inicial de la cuenta.

        Returns:
        - None
        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        try:
            self.Pregunta()
            respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea crear la cuenta {numero_cuenta}?")
            
            if respuesta == "yes":
                # Inserta en la tabla cuenta los datos enviados de la clase crearCuenta
                cursor.execute("INSERT INTO cuenta(cliente, numero_cuenta, saldo) VALUES (?, ?, ?)", (cedulaCliente, numero_cuenta, saldo))
                con.commit()
                self.Correcto()
                messagebox.showinfo("Éxito", f"La cuenta {numero_cuenta} se registró correctamente")
            else:
                self.Error()
                messagebox.showinfo("Cancelación", "Operación de creación de cuenta cancelada")

        except Exception as e:
             # En caso de error, se revierte cualquier cambio no confirmado en la base de datos
            con.rollback() 
            self.Error()
            messagebox.showerror("Error", f"Error al crear la cuenta: {str(e)}")
        finally:
            miConexion.cerrarConexion()


    
    def EliminarCuenta(self, numero_cuenta):
        """
        Elimina una cuenta de la base de datos.

        Args:
        - numero_cuenta (str): Número de cuenta que se desea eliminar.

        Returns:
        - None
        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        try:
            self.Pregunta()
            respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea eliminar la cuenta {numero_cuenta}?")
            
            if respuesta == "yes":
                 # Deshabilita las restricciones de clave externa para permitir la eliminación sin conflictos
                cursor.execute("SET foreign_key_checks = 0;")
                con.commit() 
                 # Elimina la cuenta de la tabla 'cuenta' en la base de datos
                cursor.execute("DELETE from cuenta WHERE numero_cuenta= ?", (numero_cuenta,))
                con.commit()    # Confirma la transacción en la base de datos
                self.Correcto()
                messagebox.showinfo("Éxito", f"La cuenta {numero_cuenta} se eliminó correctamente")
            else:
                self.Error()
                messagebox.showinfo("Cancelación", "Operación de eliminación cancelada")

        except Exception as e:
            # En caso de error, se revierte cualquier cambio no confirmado en la base de datos
            con.rollback() 
            self.Error()
            messagebox.showerror("Error", f"Error al eliminar la cuenta: {str(e)}")
        finally:
             # Restaura las restricciones de clave externa para mantener la integridad de los datos
            cursor.execute("SET foreign_key_checks = 1;")
            con.commit()
            miConexion.cerrarConexion()

    def buscarCuenta(self, identificador):
        """
        Busca una cuenta en la base de datos según el identificador proporcionado.

        Este método busca una cuenta bancaria en la base de datos, ya sea por el número de cuenta o por la identificación del cliente asociado.

        Args:
        - identificador (str): El número de cuenta o la identificación del cliente asociado a la cuenta que se desea buscar.

        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        try:
            # Se verifica si el identificador pertenece a un cliente registrado
            cursor.execute("SELECT usuario FROM cliente WHERE usuario = ?", (identificador,))
            resultado = cursor.fetchone()

            if resultado:
                # Si el identificador pertenece a un cliente, se verifica si ya tiene una cuenta asociada
                cursor.execute("SELECT cliente FROM cuenta JOIN cliente ON cuenta.cliente = cliente.usuario WHERE cliente.usuario = ?", (identificador,))
                listaCuentas = cursor.fetchall()

                if len(listaCuentas) > 0:
                    # Si el cliente ya tiene una cuenta asociada, se muestra una advertencia
                    self.Error()
                    messagebox.showwarning("Advertencia", f"El cliente {identificador} ya tiene una cuenta")
                else:
                    # Si el cliente no tiene cuenta asociada, se retorna None
                    return None
            else:
                # Si el identificador no pertenece a un cliente, se busca la cuenta directamente por su número de cuenta
                cursor.execute("SELECT cuenta.cliente, cuenta.saldo FROM cuenta LEFT JOIN cliente ON cuenta.cliente = cliente.usuario WHERE cuenta.numero_cuenta = ?", (identificador,))
                listaCuenta = cursor.fetchall()

                if len(listaCuenta) > 0:
                    # Si se encuentra la cuenta, se crea un objeto Cuenta con la información obtenida y se retorna
                    cuenta = listaCuenta[0]
                    cuenta2 = Cuenta(cuenta[0], cuenta[1])
                    return cuenta2
                else:
                    self.Error()
                    messagebox.showwarning("Advertencia", f"La cuenta o el cliente {identificador} no se encontró")
                    return not None

        except Exception as e:
            # En caso de error, se maneja la excepción mostrando un mensaje de error detallado
            self.Error()
            messagebox.showerror("Error", f"Error al buscar cuenta: {str(e)}")
        miConexion.cerrarConexion()

    def Deposito(self, numero_transaccion, monto, numero_cuenta):
        """
        Realiza un depósito en la cuenta bancaria especificada.

        Este método realiza un depósito en la cuenta bancaria identificada por `numero_cuenta`, actualizando el saldo y registrando la transacción correspondiente en la base de datos.

        Args:
        - numero_transaccion (int): Número único de transacción para identificar el depósito.
        - monto (float or str): Monto a depositar en la cuenta.
        - numero_cuenta (str): Número de cuenta en la que se realizará el depósito

        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        # Validación del monto ingresado
        if not monto:
            self.Error()
            messagebox.showwarning("Advertencia", "Ingrese un monto válido para realizar el depósito.")
            return

        try:
            monto = float(monto)  # Intenta convertir el monto a float
        except ValueError:
            self.Error()
            messagebox.showerror("Error", "El monto ingresado no es válido.")
            return

        try:
            # Consulta para obtener el saldo actual de la cuenta
            cursor.execute("SELECT saldo FROM cuenta WHERE numero_cuenta = ?", (numero_cuenta,))
            saldo_resultado = cursor.fetchone()

            if saldo_resultado:
                saldo_actual = saldo_resultado[0]  # Se obtiene el saldo actual de la cuenta
                nuevo_saldo = saldo_actual + monto  # Se calcula el nuevo saldo después del depósito

                # Actualización del saldo en la base de datos
                cursor.execute("UPDATE cuenta SET saldo = ? WHERE numero_cuenta = ?", (nuevo_saldo, numero_cuenta))
                con.commit()

                # Registro de la transacción de depósito en la tabla 'transaccion'
                cursor.execute("INSERT INTO transaccion(numero_transaccion, tipo, monto, cuenta) VALUES (?, 'Depósito', ?, ?)", (numero_transaccion, monto, numero_cuenta))
                con.commit()

                # Confirmación final del depósito con el usuario
                self.Pregunta()
                respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea depositar ${monto}?")

                if respuesta == "yes":
                    self.Correcto()
                    messagebox.showinfo("Éxito", f"Se ha realizado el depósito de ${monto}. Nuevo saldo: ${nuevo_saldo}")
            else:
                # Si no se encuentra la cuenta, muestra una advertencia
                self.Error()
                messagebox.showwarning("Advertencia", "No se encontró la cuenta especificada.")

        except Exception as e:
            # En caso de error, se maneja la excepción mostrando un mensaje detallado
            con.rollback() 
            self.Error()
            messagebox.showerror("Error", f"Error al realizar el depósito: {str(e)}")

        finally:
            # Se cierra la conexión con la base de datos, independientemente del resultado
            miConexion.cerrarConexion()


    def Retiro(self, numero_transaccion, monto, numero_cuenta):
        """
        Realiza un retiro desde la cuenta bancaria especificada.

        Este método realiza un retiro desde la cuenta bancaria identificada por `numero_cuenta`, actualizando el saldo y registrando la transacción correspondiente en la base de datos.

        Args:
        - numero_transaccion (int): Número único de transacción para identificar el retiro.
        - monto (float or str): Monto a retirar de la cuenta.
        - numero_cuenta (str): Número de cuenta desde la que se realizará el retiro.

        """
        miConexion = ConexionUsuario()  # Instancia de la clase para gestionar la conexión a la base de datos
        miConexion.crearConexion()      # Se abre la conexión con la base de datos
        con = miConexion.getConexion()  # Se obtiene el objeto de conexión
        cursor = con.cursor()           # Se crea un cursor para ejecutar consultas SQL

        # Validación del monto ingresado
        if not monto:
            self.Error()
            messagebox.showwarning("Advertencia", "Ingrese un monto válido para realizar el retiro.")
            return

        try:
            monto = float(monto)  # Intenta convertir el monto a float
        except ValueError:
            self.Error()
            messagebox.showerror("Error", "El monto ingresado no es válido.")
            return

        try:
            # Consulta para obtener el saldo actual de la cuenta
            cursor.execute("SELECT saldo FROM cuenta WHERE numero_cuenta = ?", (numero_cuenta,))
            saldo_resultado = cursor.fetchone()

            if saldo_resultado:
                saldo_actual = saldo_resultado[0]  # Se obtiene el saldo actual de la cuenta

                # Verifica si el saldo actual es suficiente para realizar el retiro
                if saldo_actual >= monto:
                    nuevo_saldo = saldo_actual - monto  # Calcula el nuevo saldo después del retiro

                    # Actualización del saldo en la base de datos
                    cursor.execute("UPDATE cuenta SET saldo = ? WHERE numero_cuenta = ?", (nuevo_saldo, numero_cuenta))
                    con.commit()

                    # Registro de la transacción de retiro en la tabla 'transaccion'
                    cursor.execute("INSERT INTO transaccion(numero_transaccion, tipo, monto, cuenta) VALUES (?, 'Retiro', ?, ?)", (numero_transaccion, monto, numero_cuenta))
                    con.commit()

                    # Confirmación final del retiro con el usuario
                    self.Pregunta()
                    respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea retirar ${monto}?")

                    if respuesta == "yes":
                        self.Correcto()
                        messagebox.showinfo("Éxito", f"Se ha realizado el retiro de ${monto}. Nuevo saldo: ${nuevo_saldo}")
                else:
                    # Si el monto a retirar es mayor al saldo actual, muestra una advertencia
                    self.Error()
                    messagebox.showwarning("Advertencia", "El monto que desea retirar es mayor a su saldo actual.")
            else:
                # Si no se encuentra la cuenta, muestra una advertencia
                self.Error()
                messagebox.showwarning("Advertencia", "No se encontró la cuenta especificada.")

        except Exception as e:
            # En caso de error, se maneja la excepción mostrando un mensaje detallado
            con.rollback() 
            self.Error()
            messagebox.showerror("Error", f"Error al realizar el retiro: {str(e)}")

        finally:
            # Se cierra la conexión con la base de datos, independientemente del resultado
            miConexion.cerrarConexion()

    def Error(self):
        """
        Reproduce un sonido de error utilizando hilos.

        Este método inicia un hilo que reproduce un archivo de sonido de error cuando es llamado.

        Example:
            Error()

        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\error (online-audio-converter.com).mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Correcto(self):
        """
        Reproduce un sonido de éxito utilizando hilos.

        Este método inicia un hilo que reproduce un archivo de sonido de éxito cuando es llamado.

        Example:
            Correcto()

        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\correcto.mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Inicio(self):
        """
        Reroduce un sonido de inicio utilizando hilos.

        Este método inicia un hilo que reproduce un archivo de sonido de inicio cuando es llamado.

        Example:
            Inicio()

        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\inicio.mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Pregunta(self):
        """
        Reproduce un sonido de pregunta utilizando hilos.

        Este método inicia un hilo que reproduce un archivo de sonido de pregunta cuando es llamado.

        Example:
            Pregunta()

        """
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()
