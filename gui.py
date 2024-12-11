# Importaciones de archivos y librerías
from tkinter import *
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
from tkinter import messagebox
import conectarDB
from backup import guardar_backup_txt 


# Paleta de colores y fuentes
COLOR_PRINCIPAL = "#5C6BC0"  # Azul claro brillante para botones y fondos (más suave y estético)
COLOR_SECUNDARIO = "#FF7043"  # Naranja suave (menos brillante y más armonioso)
COLOR_FONDO = "#2E3B4E"  # Fondo oscuro para la ventana principal
COLOR_FONDO_SECUNDARIO = "#3F4D63"
COLOR_TEXTO = "#FFFFFF"  # Blanco para texto
COLOR_ROJO = "#D32F2F" 
COLOR_VERDE = "#66BB6A"  
FUENTE_TITULO = ("Roboto", 24, "bold")
FUENTE_SUBTITULO = ("Roboto", 18, "bold")
FUENTE_BOTON = ("Roboto", 14)
FUENTE_ENTRY = ("Roboto", 14)

class CabanasUI:
    def __init__(self, reserva, conexion) -> None:
        self.reserva = reserva
        self.conexion = conexion
        self.ventanaHome = tk.Tk()
        self.ventanaHome.title("Gestión de reservas")
        self.ventanaHome.state("zoomed")  # Pantalla completa
        self.ventanaHome.configure(bg=COLOR_FONDO)  # Color de fondo de la ventana

        # Título
        self.titulo = tk.Label(self.ventanaHome, text="Reservas Casa de Verano", font=FUENTE_TITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.titulo.pack(pady=20)

        # Botones para las funciones principales
        self.boton_disponibilidad = tk.Button(
            self.ventanaHome, text="Mostrar disponibilidad", font=FUENTE_BOTON, bg=COLOR_PRINCIPAL, fg=COLOR_TEXTO,
            command=self.ventanaMostrar_disponibilidad
        )
        self.boton_disponibilidad.pack(pady=10)

        self.boton_ventanaReservar = tk.Button(
            self.ventanaHome, text="Insertar reserva", font=FUENTE_BOTON, bg=COLOR_VERDE, fg=COLOR_TEXTO,
            command=self.ventanaReservar
        )
        self.boton_ventanaReservar.pack(pady=10)

        self.boton_cancelar = tk.Button(
            self.ventanaHome, text="Cancelar reserva", font=FUENTE_BOTON, bg=COLOR_ROJO, fg=COLOR_TEXTO,
            command=self.ventanaCancelar_reserva
        )
        self.boton_cancelar.pack(pady=10)

        self.ventanaHome.mainloop()

    def ventanaMostrar_disponibilidad(self):
        self.ventanaMostrar_disponibilidad = tk.Tk()
        self.ventanaMostrar_disponibilidad.title("Disponibilidad")
        self.ventanaMostrar_disponibilidad.state("zoomed")
        self.ventanaMostrar_disponibilidad.configure(bg=COLOR_FONDO)

        self.titulo = tk.Label(self.ventanaMostrar_disponibilidad, text="Disponibilidad para reservas", font=FUENTE_TITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.titulo.pack(pady=20)

        # Crear un frame (contenedor) para el calendario y la lista de reservas
        frame_principal = tk.Frame(self.ventanaMostrar_disponibilidad, bg=COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=False, padx=150, pady=(20, 100))

        # Crear un frame para el calendario (a la izquierda)
        frame_calendario = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_calendario.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Título del calendario
        self.titulo_calendario = tk.Label(frame_calendario, text="Calendario", font=FUENTE_SUBTITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.titulo_calendario.pack(pady=5)
        # Calendario con estilo personalizado
        calendario = Calendar(
            frame_calendario,
            date_pattern="yyyy-MM-dd",
            font=FUENTE_ENTRY,
            background=COLOR_PRINCIPAL,
            foreground=COLOR_TEXTO,
            headersbackground=COLOR_FONDO_SECUNDARIO,  # Fondo de los encabezados (días de la semana)
            headersforeground=COLOR_TEXTO,  # Texto de los encabezados
            selectbackground=COLOR_SECUNDARIO,  # Color de selección
            selectforeground=COLOR_TEXTO,  # Texto de la selección
            bordercolor=COLOR_FONDO_SECUNDARIO,  # Borde del calendario
            showweeknumbers=False  # Ocultar números de semana
        )
        calendario.pack(pady=10)

        # Obtener fechas ocupadas desde la base de datos
        fechas_ocupadas = conectarDB.obtenerFechasOcupadas(self.conexion)
        fechas_reservadas = []
        # Generar todas las fechas ocupadas entre FechaEntrada y FechaSalida
        for reserva in fechas_ocupadas:
            inicio = reserva['FechaEntrada']
            fin = reserva['FechaSalida']
            while inicio < fin:
                fechas_reservadas.append(inicio.strftime("%Y-%m-%d"))
                inicio += timedelta(days=1)

        # Agregar etiqueta a las fechas reservadas
        for fecha in fechas_reservadas:
            calendario.calevent_create(datetime.strptime(fecha, "%Y-%m-%d"), "Ocupado", "ocupado")

        # Darle un fondo rojo a las fechas etiquetadas
        calendario.tag_config("ocupado", background=COLOR_ROJO, foreground=COLOR_TEXTO)


        # Crear un contenedor para la lista de reservas (a la derecha)
        frame_lista_reservas = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_lista_reservas.pack(side=tk.RIGHT,  padx=5)

        # Título de la lista de reservas
        self.titulo_reservas = tk.Label(frame_lista_reservas, text="Lista de Reservas", font=FUENTE_SUBTITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.titulo_reservas.pack(pady=5)

        # Obtener reservas de la base de datos
        reservas = conectarDB.obtenerReservas(self.conexion)

        # Crear la lista de reservas
        self.lista_reservas = tk.Listbox(frame_lista_reservas, width=50, height=10, font=FUENTE_ENTRY, bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO)
        
        # Crear el Scrollbar
        scrollbar = tk.Scrollbar(frame_lista_reservas, orient=tk.VERTICAL, command=self.lista_reservas.yview)
        self.lista_reservas.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        scrollbar.config(width=12)
        # Mostrar las reservas en la lista
        for reserva in reservas:
            self.lista_reservas.insert(tk.END, f" {reserva['NombreCompletoCliente']} - {reserva['FechaEntrada']} a {reserva['FechaSalida']} ")
        self.lista_reservas.pack()

        self.crearBtnCerrar(self.ventanaMostrar_disponibilidad)

    def ventanaReservar(self):
        self.ventanaReservar = tk.Tk()
        self.ventanaReservar.title("Reservar")
        self.ventanaReservar.state("zoomed")
        self.ventanaReservar.configure(bg=COLOR_FONDO)

        # Título principal
        self.titulo = tk.Label(self.ventanaReservar, text="Complete los datos para la reserva", font=FUENTE_TITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.titulo.pack(pady=20)

        # Frame contenedor del formulario
        frame_formulario = tk.Frame(self.ventanaReservar, bg=COLOR_FONDO_SECUNDARIO, bd=2, relief=tk.GROOVE)
        frame_formulario.pack(pady=20, padx=20, ipadx=10, ipady=10)

        # Nombre del cliente
        txtNombre = tk.Label(frame_formulario, text="Nombre completo del cliente:", fg=COLOR_TEXTO, font=FUENTE_SUBTITULO, bg=COLOR_FONDO_SECUNDARIO)
        txtNombre.pack(pady=10, padx=20, anchor="w")
        entryNombre = tk.Entry(frame_formulario, background="white", font=FUENTE_ENTRY)
        entryNombre.pack(pady=5, padx=20, fill=tk.X)

        # Fecha de entrada
        txtFechaEntrada = tk.Label(frame_formulario, text="Fecha de entrada:", fg=COLOR_TEXTO, font=FUENTE_SUBTITULO, bg=COLOR_FONDO_SECUNDARIO)
        txtFechaEntrada.pack(pady=10, padx=20, anchor="w")
        entryFechaEntrada = DateEntry(
            frame_formulario, date_pattern="yyyy-MM-dd", background="white", 
            foreground="black", font=FUENTE_ENTRY, width=15
        )
        entryFechaEntrada.pack(pady=5)

        # Fecha de salida
        txtFechaSalida = tk.Label(frame_formulario, text="Fecha de salida:", fg=COLOR_TEXTO, font=FUENTE_SUBTITULO, bg=COLOR_FONDO_SECUNDARIO)
        txtFechaSalida.pack(pady=10, padx=20, anchor="w")
        entryFechaSalida = DateEntry(
            frame_formulario, date_pattern="yyyy-MM-dd", background="white", 
            foreground="black", font=FUENTE_ENTRY, width=15
        )
        entryFechaSalida.pack(pady=5)

        # Función para guardar la reserva
        def guardarReserva():
           # Se obtienen los datos desde los Entry        
            cliente = entryNombre.get()
            fecha_entrada = entryFechaEntrada.get_date()
            fecha_salida = entryFechaSalida.get_date()
           # Comprobar que no haya campos vacíos  
            if not cliente or not fecha_entrada or not fecha_salida:
                tk.messagebox.showwarning("Error", "Por favor, complete todos los campos.")
                return
           # Comprobar coherencia en las fechas
            if fecha_entrada >= fecha_salida:
                tk.messagebox.showwarning("Error", "La fecha de salida debe ser posterior a la de entrada.")
                return
                
            # Validar si las fechas ya están ocupadas
            fechas_ocupadas = conectarDB.obtenerFechasOcupadas(self.conexion)
            for fecha in fechas_ocupadas:
                if (fecha_entrada < fecha['FechaSalida'] and fecha_salida > fecha['FechaEntrada']):
                    tk.messagebox.showwarning("Error", "Las fechas seleccionadas ya están ocupadas.")
                    return
            
            from conectarDB import agregarReserva
            exito = agregarReserva(self.conexion, cliente, fecha_entrada, fecha_salida)
            
            if exito:
                tk.messagebox.showinfo("Éxito", "Reserva creada con éxito.")
                guardar_backup_txt(cliente, fecha_entrada, fecha_salida)  # Llamar la función importada
                self.cerrarVentana(self.ventanaReservar)
            else:
                tk.messagebox.showerror("Error", "No se pudo guardar la reserva. Inténtelo de nuevo.")
        
        btnConfirmar = tk.Button(
            self.ventanaReservar, text="Confirmar", font=FUENTE_BOTON, command=guardarReserva, bg=COLOR_PRINCIPAL, fg=COLOR_TEXTO
        )
        btnConfirmar.pack(pady=20)

        self.crearBtnCerrar(self.ventanaReservar)

    def ventanaCancelar_reserva(self):
        self.ventanaCancelarReserva = tk.Tk()
        self.ventanaCancelarReserva.title("Cancelar reserva")
        self.ventanaCancelarReserva.state("zoomed")
        self.ventanaCancelarReserva.configure(bg=COLOR_FONDO)

        self.titulo = tk.Label(self.ventanaCancelarReserva, text="Seleccione la reserva a cancelar", font=FUENTE_TITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.titulo.pack(pady=20)

        # Crear un frame para la lista de reservas
        frame_lista_reservas = tk.Frame(self.ventanaCancelarReserva, bg=COLOR_FONDO)
        frame_lista_reservas.pack(side=tk.TOP, padx=5, pady=5)  

        # Título de la lista de reservas
        self.titulo_reservas = tk.Label(frame_lista_reservas, text="Lista de Reservas", font=FUENTE_SUBTITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.titulo_reservas.pack(pady=5)

        # Obtener reservas de la base de datos
        reservas = conectarDB.obtenerReservas(self.conexion)

        # Crear la lista de reservas
        self.lista_reservas = tk.Listbox(frame_lista_reservas, width=50, height=15, font=FUENTE_ENTRY, bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO)
        self.lista_reservas.pack(side=tk.LEFT, fill=tk.Y, expand=True) 

        # Crear el Scrollbar
        scrollbar = tk.Scrollbar(frame_lista_reservas, orient=tk.VERTICAL, command=self.lista_reservas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5)  # Asegurar que el Scrollbar esté pegado a la derecha
        self.lista_reservas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(width=12)

        # Insertar las reservas en el Listbox
        for reserva in reservas:
            self.lista_reservas.insert(tk.END, f" {reserva['idReserva']} - {reserva['NombreCompletoCliente']} - {reserva['FechaEntrada']} a {reserva['FechaSalida']}   ")

        btnCancelar = tk.Button(self.ventanaCancelarReserva, text="Eliminar reserva", font=FUENTE_BOTON, bg=COLOR_ROJO, fg=COLOR_TEXTO, command=self.cancelar_reserva)
        btnCancelar.pack(pady=20)

        self.crearBtnCerrar(self.ventanaCancelarReserva)

        
    def cancelar_reserva(self):
        try:
            selected_index = self.lista_reservas.curselection()[0]
            reserva_seleccionada = self.lista_reservas.get(selected_index)
            idReserva = reserva_seleccionada.split(" - ")[0]

            confirmacion = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea cancelar la reserva N°:{idReserva}?")
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

    # Crear el botón Cerrar
    def crearBtnCerrar(self, ventana):
        btnCerrar = tk.Button(
            ventana, text="Cerrar", 
            command=lambda: self.cerrarVentana(ventana),
            bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO, font=FUENTE_BOTON,
            padx=1, pady=2, bd=3, relief="raised"
        )
        btnCerrar.pack(pady=5)
