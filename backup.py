def guardar_backup_txt(cliente, fecha_entrada, fecha_salida):
    # Normalizar el nombre del cliente (eliminar espacios y convertir a mayúsculas)
    cliente_normalizado = cliente.strip().upper()

    # Abrir el archivo en modo append para agregar nuevas reservas sin sobrescribir el archivo
    with open("backup_reservas.txt", "a") as archivo:
        # Escribir los detalles de la reserva en el archivo
        archivo.write(f"Cliente: {cliente_normalizado}\n")
        archivo.write(f"Fecha de entrada: {fecha_entrada.strftime('%Y-%m-%d')}\n")
        archivo.write(f"Fecha de salida: {fecha_salida.strftime('%Y-%m-%d')}\n")
        archivo.write("-" * 40 + "\n")  # Separador entre reservas

