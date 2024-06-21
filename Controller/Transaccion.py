class Transaccion():
    """
    Representa una transacción financiera realizada en un sistema de gestión bancaria.

    Attributes:
        numero_transaccion (str): Número único que identifica la transacción.
        monto (float): Monto de la transacción.
        cuenta (str): Número de cuenta asociado a la transacción.
    """

    def __init__(self, numero_transaccion="", monto="", cuenta=""):
        """
        Constructor de la clase Transaccion.

        Args:
            numero_transaccion (str, optional): Número único que identifica la transacción. 
            monto (float, optional): Monto de la transacción. 
            cuenta (str, optional): Número de cuenta asociado a la transacción. 
        """
        self.numero_transaccion = numero_transaccion
        self.monto = monto
        self.cuenta = cuenta

    def getNumero_transaccion(self):
        """
        Retorna el número único que identifica la transacción.

        Returns:
            str: Número único que identifica la transacción.
        """
        return self.numero_transaccion

    def getMonto(self):
        """
        Retorna el monto de la transacción.

        Returns:
            float: Monto de la transacción.
        """
        return self.monto

    def getCuenta(self):
        """
        Retorna el número de cuenta asociado a la transacción.

        Returns:
            str: Número de cuenta asociado a la transacción.
        """
        return self.cuenta

    def setNumero_transaccion(self, numero_transaccion):
        """
        Establece el número único que identifica la transacción.

        Args:
            numero_transaccion (str): Número único a establecer para la transacción.
        """
        self.numero_transaccion = numero_transaccion

    def setMonto(self, monto):
        """
        Establece el monto de la transacción.

        Args:
            monto (float): Monto a establecer para la transacción.
        """
        self.monto = monto

    def setCuenta(self, cuenta):
        """
        Establece el número de cuenta asociado a la transacción.

        Args:
            cuenta (str): Número de cuenta a establecer para la transacción.
        """
        self.cuenta = cuenta
