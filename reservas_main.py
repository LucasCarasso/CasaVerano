import conectarDB
from reservas_model import Reserva
import gui

basedatos = {
    'host': 'localhost',
    'usuario_sql': 'root',
    'clave_sql': 'root',
    'port': 3306
}

host = basedatos['host']
user = basedatos['usuario_sql']
password = basedatos['clave_sql']
port = basedatos['port']

cnx = conectarDB.conectar(host, user, password, port)

def leerBDD():
    reservas = conectarDB.obtenerReservas(cnx)
    print(reservas)
    arrayReservas = []

    for reserva in reservas:
        cliente = reserva['NombreCompletoCliente']
        fechaEntrada = reserva['FechaEntrada']
        fechaSalida = reserva['FechaSalida']

        nuevaReserva = Reserva(cliente, fechaEntrada, fechaSalida)
        arrayReservas.append(nuevaReserva)

    print(arrayReservas)
    return arrayReservas

rsv = leerBDD()
reservasGUI = gui.CabanasUI(rsv, cnx)

