# Clase base Cliente
class Cliente:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tarjetas_debito = []
        self.tarjetas_credito = []
        self.cuentas = []

    def agregar_tarjeta_debito(self, tarjeta):
        self.tarjetas_debito.append(tarjeta)

    def agregar_tarjeta_credito(self, tarjeta):
        self.tarjetas_credito.append(tarjeta)

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

    def info_cliente(self):
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"


# Subclase para clientes Classic
class ClienteClassic(Cliente):
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni)
        self.retiro_diario_max = 10000
        self.comision_transferencias = 0.01
        self.limite_transferencia_recibida = 150000

        # Caja de ahorro en pesos por defecto
        self.agregar_cuenta(CajaAhorroPesos())

        # Tarjeta de débito por defecto
        self.agregar_tarjeta_debito(TarjetaDebito())

    def puede_comprar_dolares(self):
        return False

    def puede_tener_chequera(self):
        return False

    def puede_tener_tarjeta_credito(self):
        return False


# Subclase para clientes Gold
class ClienteGold(Cliente):
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni)
        self.retiro_diario_max = 20000
        self.comision_transferencias = 0.005
        self.limite_transferencia_recibida = 500000
        self.descubierto_max = -10000

        # Caja de ahorro en pesos, caja de ahorro en dólares y cuenta corriente por defecto
        self.agregar_cuenta(CajaAhorroPesos())
        self.agregar_cuenta(CajaAhorroDolares())
        self.agregar_cuenta(CuentaCorriente(self.descubierto_max))

        # Tarjeta de débito por defecto
        self.agregar_tarjeta_debito(TarjetaDebito())

        # Tarjeta de crédito limitada a 1
        self.agregar_tarjeta_credito(TarjetaCredito())

    def puede_comprar_dolares(self):
        return True

    def puede_tener_chequera(self):
        return True

    def puede_tener_tarjeta_credito(self):
        return len(self.tarjetas_credito) < 1


# Subclase para clientes Black
class ClienteBlack(Cliente):
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni)
        self.retiro_diario_max = 100000
        self.comision_transferencias = 0.0
        self.limite_transferencia_recibida = float('inf')
        self.descubierto_max = -10000

        # Caja de ahorro en pesos, caja de ahorro en dólares y cuenta corriente por defecto
        self.agregar_cuenta(CajaAhorroPesos())
        self.agregar_cuenta(CajaAhorroDolares())
        self.agregar_cuenta(CuentaCorriente(self.descubierto_max))

        # Tarjeta de débito y hasta 5 tarjetas de crédito
        self.agregar_tarjeta_debito(TarjetaDebito())
        for i in range(5):
            self.agregar_tarjeta_credito(TarjetaCredito())

        # Chequera (hasta 2 chequeras)
        self.chequeras = 2

    def puede_comprar_dolares(self):
        return True

    def puede_tener_chequera(self):
        return len(self.chequeras) < 2

    def puede_tener_tarjeta_credito(self):
        return len(self.tarjetas_credito) < 5


# Clase base Cuenta
class Cuenta:
    def __init__(self, moneda, saldo=0):
        self.moneda = moneda
        self.saldo = saldo

    def depositar(self, monto):
        self.saldo += monto

    def retirar(self, monto):
        if monto <= self.saldo:
            self.saldo -= monto
        else:
            raise ValueError("Fondos insuficientes")


# Subclases para tipos de cuentas
class CajaAhorroPesos(Cuenta):
    def __init__(self, saldo=0):
        super().__init__("Pesos", saldo)


class CajaAhorroDolares(Cuenta):
    def __init__(self, saldo=0):
        super().__init__("Dólares", saldo)


class CuentaCorriente(Cuenta):
    def __init__(self, descubierto_max=-10000, saldo=0):
        super().__init__("Pesos", saldo)
        self.descubierto_max = descubierto_max

    def retirar(self, monto):
        if self.saldo - monto >= self.descubierto_max:
            self.saldo -= monto
        else:
            raise ValueError("Excede el límite de descubierto")


# Clase para tarjetas
class TarjetaDebito:
    def __init__(self):
        self.tipo = "Debito"


class TarjetaCredito:
    def __init__(self):
        self.tipo = "Credito"
