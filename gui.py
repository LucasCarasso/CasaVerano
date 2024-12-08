from tkinter import *
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
from tkinter import messagebox
import conectarDB

class CabanasUI:
    def __init__(self,reserva, conexion) -> None:
        self.reserva=reserva
        self.conexion=conexion
        self.ventanaHome = tk.Tk()
        self.ventanaHome.title("Cabañas ADETEC")
        self.ventanaHome.state("zoomed")  # Pantalla completa
        
        # Título
        self.titulo = tk.Label(self.ventanaHome, text="Casa de Verano", font=("Arial", 24, "bold"))
        self.titulo.pack(pady=20)
        
        # Botones para las funciones principales
        self.boton_disponibilidad = tk.Button(
            self.ventanaHome, text="Mostrar disponibilidad", font=("Arial", 16), command=self.ventanaMostrar_disponibilidad
        )
        self.boton_disponibilidad.pack(pady=10)

        self.boton_ventanaReservar = tk.Button(
            self.ventanaHome, text="Reservar", font=("Arial", 16), command=self.ventanaReservar
        )
        self.boton_ventanaReservar.pack(pady=10)

        self.boton_cancelar = tk.Button(
            self.ventanaHome, text="Cancelar reserva", font=("Arial", 16), command=self.ventanaCancelar_reserva
        )
        self.boton_cancelar.pack(pady=10)

        self.ventanaHome.mainloop()

    def ventanaMostrar_disponibilidad(self):
        self.ventanaMostrar_disponibilidad = tk.Tk()
        self.ventanaMostrar_disponibilidad.title("Disponibilidad")
        self.ventanaMostrar_disponibilidad.state("zoomed")

        self.titulo= tk.Label(self.ventanaMostrar_disponibilidad, text="Disponibilidad para reservas", font=("Arial", 24, "bold"))
        self.titulo.pack(pady=20)

        calendario = Calendar(self.ventanaMostrar_disponibilidad, date_pattern="yyyy-MM-dd", font=("Arial", 14))
        calendario.pack(pady=20)

        # Obtener fechas ocupadas desde la base de datos
        from conectarDB import obtenerFechasOcupadas
        fechas_ocupadas = obtenerFechasOcupadas(self.conexion)
        fechas_reservadas = []

        # Generar todas las fechas ocupadas entre FechaEntrada y FechaSalida
        for reserva in fechas_ocupadas:
            inicio = reserva['FechaEntrada']
            fin = reserva['FechaSalida']
            while inicio <= fin:
                fechas_reservadas.append(inicio.strftime("%Y-%m-%d"))
                inicio += timedelta(days=1)

            # Agregar etiqueta a las fechas reservadas
            for fecha in fechas_reservadas:
                calendario.calevent_create(datetime.strptime(fecha, "%Y-%m-%d"), "Ocupado", "ocupado")

            # Darle un fondo rojo a las fechas etiquetadas
            calendario.tag_config("ocupado", background="red", foreground="white")

        # Botón cerrar
        self.crearBtnCerrar(self.ventanaMostrar_disponibilidad)

    def ventanaReservar(self):
        self.ventanaReservar = tk.Tk()
        self.ventanaReservar.title("Reservar")
        self.ventanaReservar.state("zoomed")

        self.titulo = tk.Label(
            self.ventanaReservar, text="Complete los datos para la reserva", font=("Arial", 24, "bold")
        )
        self.titulo.pack(pady=20)

        # Nombre del cliente
        txtNombre = tk.Label(self.ventanaReservar, text="Nombre completo del cliente:", fg="black", font=("Arial", 18, "bold"))
        txtNombre.pack(pady=10)
        entryNombre = tk.Entry(self.ventanaReservar, background="white", font=("Arial", 14))
        entryNombre.pack(pady=5)

        # Fecha de entrada
        txtFechaEntrada = tk.Label(self.ventanaReservar, text="Fecha de entrada:", fg="black", font=("Arial", 18, "bold"))
        txtFechaEntrada.pack(pady=10)
        entryFechaEntrada = DateEntry(
            self.ventanaReservar, date_pattern="yyyy-MM-dd", background="white", foreground="black", font=("Arial", 14), width=15
        )
        entryFechaEntrada.pack(pady=5)

        # Fecha de salida
        txtFechaSalida = tk.Label(self.ventanaReservar, text="Fecha de salida:", fg="black", font=("Arial", 18, "bold"))
        txtFechaSalida.pack(pady=10)
        entryFechaSalida = DateEntry(
            self.ventanaReservar, date_pattern="yyyy-MM-dd", background="white", foreground="black", font=("Arial", 14), width=15
        )
        entryFechaSalida.pack(pady=5)

        def guardarReserva():
            cliente = entryNombre.get()
            fecha_entrada = entryFechaEntrada.get_date()
            fecha_salida = entryFechaSalida.get_date()

            if not cliente or not fecha_entrada or not fecha_salida:
                tk.messagebox.showwarning("Error", "Por favor, complete todos los campos.")
                return

            if fecha_entrada >= fecha_salida:
                tk.messagebox.showwarning("Error", "La fecha de salida debe ser posterior a la de entrada.")
                return

            from conectarDB import agregarReserva
            exito = agregarReserva(self.conexion, cliente, fecha_entrada, fecha_salida)

            if exito:
                tk.messagebox.showinfo("Éxito", "Reserva creada con éxito.")
                self.cerrarVentana(self.ventanaReservar)
            else:
                tk.messagebox.showerror("Error", "No se pudo guardar la reserva. Inténtelo de nuevo.")

        btnConfirmar = tk.Button(
            self.ventanaReservar, text="Confirmar", font=("Arial", 16), command=guardarReserva, bg="green", fg="white"
        )
        btnConfirmar.pack(pady=20)

        self.crearBtnCerrar(self.ventanaReservar)

    def ventanaCancelar_reserva(self):
        self.ventanaCancelarReserva = tk.Tk()
        self.ventanaCancelarReserva.title("Cancelar reserva")
        self.ventanaCancelarReserva.state("zoomed")

        self.titulo= tk.Label(self.ventanaCancelarReserva, text="Seleccione la reserva a cancelar", font=("Arial", 24, "bold"))
        self.titulo.pack(pady=20)

        reservas = conectarDB.obtenerReservas(self.conexion)

        self.lista_reservas = tk.Listbox(self.ventanaCancelarReserva, width=50, height=15, font=("Arial", 14))
        for reserva in reservas:
            self.lista_reservas.insert(tk.END, f"{reserva['idReserva']} - {reserva['NombreCompletoCliente']} - {reserva['FechaEntrada']} a {reserva['FechaSalida']}")
        self.lista_reservas.pack(pady=10)
        
        btnCancelar = tk.Button(self.ventanaCancelarReserva, text="Cancelar reserva", font=("Arial", 16), command=self.cancelar_reserva)
        btnCancelar.pack(pady=20)

        self.crearBtnCerrar(self.ventanaCancelarReserva)
        
    def cancelar_reserva(self):
            try:
                selected_index = self.lista_reservas.curselection()[0]
                reserva_seleccionada = self.lista_reservas.get(selected_index)
                idReserva = reserva_seleccionada.split(" - ")[0]

                confirmacion = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea cancelar la reserva {idReserva}?")
                if confirmacion:
                    exito = conectarDB.eliminarReserva(self.conexion, idReserva)
                    if exito:
                        messagebox.showinfo("Éxito", "Reserva cancelada con éxito.")
                        self.cerrarVentana(self.ventanaCancelarReserva)
                    else:
                        messagebox.showerror("Error", "No se pudo cancelar la reserva. Inténtelo de nuevo.")
            except IndexError:
                messagebox.showwarning("Error", "Por favor, seleccione una reserva para cancelar.")

    def cerrarVentana(self, ventana):
        ventana.destroy()

    def crearBtnCerrar(self, ventana):
        btnCerrar = tk.Button(
            ventana, text="Cerrar", 
            command=lambda: self.cerrarVentana(ventana),
            bg="#6A7FAD", fg="white", font=("Helvetica", 10, "bold"),
            padx=1, pady=2, bd=3, relief="raised"
        )
        btnCerrar.pack(pady=5)


    