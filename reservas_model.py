class Reserva:
    """Crea el objeto reserva con el cliente y las fechas."""
    def __init__(self, cliente, fecha_entrada, fecha_salida):
        self.cliente = cliente
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida