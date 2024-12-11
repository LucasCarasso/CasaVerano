import pymysql

def conectar(host, user, password, port):
    conexion = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database='reservas',
            cursorclass=pymysql.cursors.DictCursor
        )
    return conexion

def agregarReserva(conexion, cliente, fecha_entrada, fecha_salida):
    try:
        # Normalizar el nombre del cliente: pasar a mayúsculas y quitar espacios al principio y final.
        cliente = cliente.strip().upper()
        with conexion.cursor() as cursor:
            cursor.execute("USE reservas;")
            consulta = """
                INSERT INTO Reservas (NombreCompletoCliente, FechaEntrada, FechaSalida)
                VALUES (%s, %s, %s);
            """
            cursor.execute(consulta, (cliente, fecha_entrada, fecha_salida))
            conexion.commit()
            return True
    except pymysql.MySQLError as err:
        print(f"Error al insertar reserva: {err}")
        return False

def obtenerReservas(conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT idReserva,NombreCompletoCliente,FechaEntrada,FechaSalida FROM reservas ORDER BY FechaEntrada")
            return cursor.fetchall() 
    except Exception as e:
        print(f"Error al obtener las reservas: {e}")
        return []

def eliminarReserva(conexion, idReserva):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM reservas WHERE idReserva = %s", (idReserva,))
            conexion.commit()
            return True
    except Exception as e:
        print(f"Error al eliminar la reserva: {e}")
        return False

def obtenerFechasOcupadas(conexion):
    try:
        with conexion.cursor() as cursor:
            consulta = "SELECT FechaEntrada, FechaSalida FROM Reservas;"
            cursor.execute(consulta)
            fechas = cursor.fetchall()
            return fechas
    except Exception as e:
        print(f"Error al obtener las fechas ocupadas: {e}")
        return []
