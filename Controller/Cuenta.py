class Cuenta():
    """
    Representa una cuenta asociada a un cliente en un sistema de gestión financiera.

    Attributes:
        cliente (str): Cliente asociado a la cuenta.
        saldo (float): Saldo actual de la cuenta.
        numero_cuenta (str): Número único que identifica la cuenta.
    """

    def __init__(self, cliente="", saldo="", numero_cuenta=""):
        """
        Constructor de la clase Cuenta.

        Args:
            cliente (str, optional): Cliente asociado a la cuenta.
            saldo (float, optional): Saldo actual de la cuenta. 
            numero_cuenta (str, optional): Número único que identifica la cuenta. 
        """
        self.cliente = cliente
        self.saldo = saldo
        self.numero_cuenta = numero_cuenta

    def getCliente(self):
        """
        Retorna el cliente asociado a la cuenta.

        Returns:
            str: Cliente asociado a la cuenta.
        """
        return self.cliente

    def getSaldo(self):
        """
        Retorna el saldo actual de la cuenta.

        Returns:
            float: Saldo actual de la cuenta.
        """
        return self.saldo

    def getNumero_cuenta(self):
        """
        Retorna el número único que identifica la cuenta.

        Returns:
            str: Número único que identifica la cuenta.
        """
        return self.numero_cuenta

    def setCliente(self, cliente):
        """
        Establece el cliente asociado a la cuenta.

        Args:
            cliente (str): Cliente a establecer para la cuenta.
        """
        self.cliente = cliente

    def setSaldo(self, saldo):
        """
        Establece el saldo actual de la cuenta.

        Args:
            saldo (float): Saldo a establecer para la cuenta.
        """
        self.saldo = saldo

    def setNumero_cuenta(self, numero_cuenta):
        """
        Establece el número único que identifica la cuenta.

        Args:
            numero_cuenta (str): Número único a establecer para la cuenta.
        """
        self.numero_cuenta = numero_cuenta
