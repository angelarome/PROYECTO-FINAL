class Usuario():
    """
    Representa un usuario en un sistema de gestión, con atributos como cédula, nombre, apellido, teléfono y correo electrónico.

    Attributes:
        cedula (str): Número de identificación del usuario.
        nombre (str): Nombre del usuario.
        apellido (str): Apellido del usuario.
        telefono (str): Número de teléfono del usuario.
        email (str): Correo electrónico del usuario.

    """

    def __init__(self, cedula="", nombre="", apellido="", telefono="", email=""):
        """
        Constructor de la clase Usuario.

        Args:
            cedula (str, optional): Número de identificación del usuario. 
            nombre (str, optional): Nombre del usuario. 
            apellido (str, optional): Apellido del usuario. 
            telefono (str, optional): Número de teléfono del usuario.
            email (str, optional): Correo electrónico del usuario. 
        """
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def getCedula(self):
        """
        Retorna el número de cédula del usuario.

        Returns:
            str: Número de cédula del usuario.
        """
        return self.cedula

    def getNombre(self):
        """
        Retorna el nombre del usuario.

        Returns:
            str: Nombre del usuario.
        """
        return self.nombre

    def getApellido(self):
        """
        Retorna el apellido del usuario.

        Returns:
            str: Apellido del usuario.
        """
        return self.apellido

    def getTelefono(self):
        """
        Retorna el número de teléfono del usuario.

        Returns:
            str: Número de teléfono del usuario.
        """
        return self.telefono

    def getEmail(self):
        """
        Retorna el correo electrónico del usuario.

        Returns:
            str: Correo electrónico del usuario.
        """
        return self.email

    def setCedula(self, cedula):
        """
        Establece el número de cédula del usuario.

        Args:
            cedula (str): Número de cédula a establecer para el usuario.
        """
        self.cedula = cedula

    def setNombre(self, nombre):
        """
        Establece el nombre del usuario.

        Args:
            nombre (str): Nombre a establecer para el usuario.
        """
        self.nombre = nombre

    def setApellido(self, apellido):
        """
        Establece el apellido del usuario.

        Args:
            apellido (str): Apellido a establecer para el usuario.
        """
        self.apellido = apellido

    def setTelefono(self, telefono):
        """
        Establece el número de teléfono del usuario.

        Args:
            telefono (str): Número de teléfono a establecer para el usuario.
        """
        self.telefono = telefono

    def setEmail(self, email):
        """
        Establece el correo electrónico del usuario.

        Args:
            email (str): Correo electrónico a establecer para el usuario.
        """
        self.email = email
