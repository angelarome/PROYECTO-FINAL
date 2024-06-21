from Controller.Usuario import Usuario

class Cliente(Usuario):
    def __init__(self, cedula="", nombre="", apellido="", telefono="", email=""):
        """
        Constructor de la clase Cliente.
        
        Args:
        - cedula (str): Cédula del cliente.
        - nombre (str): Nombre del cliente.
        - apellido (str): Apellido del cliente.
        - telefono (str): Número de teléfono del cliente.
        - email (str): Dirección de correo electrónico del cliente.
        """
        # Llama al constructor de la clase base Usuario
        Usuario.__init__(self, cedula, nombre, apellido, telefono, email)
        
        # Atributos privados de la clase Cliente
        self.__cedula = cedula
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email
    
    # Métodos getter para obtener los atributos privados
    def getCedula(self):
        """Devuelve la cédula del cliente."""
        return self.__cedula
    
    def getNombre(self):
        """Devuelve el nombre del cliente."""
        return self.__nombre
    
    def getApellido(self):
        """Devuelve el apellido del cliente."""
        return self.__apellido
    
    def getTelefono(self):
        """Devuelve el número de teléfono del cliente."""
        return self.__telefono
    
    def getEmail(self):
        """Devuelve el correo electrónico del cliente."""
        return self.__email
    
    # Métodos setter para establecer los atributos privados
    def setCedula(self, cedula):
        """
        Establece la cédula del cliente.
        
        Args:
        - cedula (str): Nueva cédula del cliente.
        """
        self.__cedula = cedula
    
    def setNombre(self, nombre):
        """
        Establece el nombre del cliente.
        
        Args:
        - nombre (str): Nuevo nombre del cliente.
        """
        self.__nombre = nombre
    
    def setApellido(self, apellido):
        """
        Establece el apellido del cliente.
        
        Args:
        - apellido (str): Nuevo apellido del cliente.
        """
        self.__apellido = apellido
    
    def setTelefono(self, telefono):
        """
        Establece el número de teléfono del cliente.
        
        Args:
        - telefono (str): Nuevo número de teléfono del cliente.
        """
        self.__telefono = telefono
    
    def setEmail(self, email):
        """
        Establece el correo electrónico del cliente.
        
        Args:
        - email (str): Nueva dirección de correo electrónico del cliente.
        """
        self.__email = email
