### SISTEMA DE RESERVAS PARA CABAÑA

## DESCRIPCIÓN DEL PROYECTO
La aplicación fue desarrollada en Python con una interfaz gráfica usando "tkinter" y persistencia de datos a través de MySQL. Su objetivo es simplificar la administración de reservas para un alojamiento, permitiendo a los usuarios realizar operaciones básicas como agregar, visualizar y eliminar reservas.

---

### FUNCIONALIDADES PRINCIPALES

1. **AGREGAR RESERVAS**: Los usuarios pueden agregar reservas mediante un formulario de entrada con validación de datos obligatorios.

2. **VISUALIZAR RESERVAS**: Se muestran todas las reservas existentes en una lista ordenada junto a un calendario con las fechas disponibles y ocupadas.

3. **ELIMINAR RESERVAS**: Se permite eliminar una reserva en caso de que haya sido cancelada.

4. **PERSISTENCIA DE DATOS**: La información se almacena de manera permanente en una base de datos MySQL.

5. **INTERFAZ GRÁFICA**: Diseño intuitivo utilizando la librería "tkinter", facilitando la experiencia del usuario.

---

### REQUISITOS TÉCNICOS
- **Lenguaje de Programación**: Python 3.8 o superior.
- **Base de Datos**: MySQL.
- **Librerías Necesarias**:
  - `tkinter` (para visualizar la interfaz gráfica).
  - `pymysql` (para conectar a la base de datos MySQL).
  - `tkcalendar` (para poder mostrar los datos en un calendario).

## CONFIGURACIÓN DEL SISTEMA
1.Instalar Python: Tener Python 3.8 o superior instalado. Se puede descargar desde python.org.

2.Instalar MySQL: Configure un servidor MySQL. Se puede descargar desde mysql.com.

3.Instalar librerías necesarias: Abrir CMD y ejecutar el siguiente comando: pip install pymysql tkcalendar

4.Crear Base de Datos: Ejecutar el script BDD.txt en MySQL.

---

## INSTRUCCIONES DE USO

 **Funcionalidades**:
   - **Botón Mostrar Disponibilidad**: Se visualizarán las reservas listadas junto a un calendario con las fechas disponibles y ocupadas.
   - **Botón Insertar Reserva**: Complete el formulario con los datos requeridos y presione "Confirmar".
   - **Botón Cancelar Reserva**: Seleccione una reserva de la lista y presione el botón "Eliminar reserva".

---

## POSIBLES ERRORES Y SOLUCIONES

- **Error al agregar una reserva**: Asegúrese de completar todos los campos.
- **Interfaz no muestra datos**: Verifique que el servidor MySQL esté activo y que las credenciales sean correctas.
- **Error al eliminar una reserva**: Asegúrese de seleccionar una reserva de la lista.

---

## ESTRUCTURA DEL PROYECTO

CasaVerano/
|-- backup_reservas.txt    # Archivo donde se guardan las reservas insertadas a modo de backup.
|-- backup.py              # Archivo que contiene la función para generar y guardar el backup.
|-- BDD.txt                # Archivo que contiene el script para crear la base de datos.
|-- conectarDB.py          # Archivo que gestiona las funciones relacionadas a la base de datos MySQL.
|-- gui.py                 # Archivo que contiene la interfaz gráfica.
|-- README.txt             # Instrucciones de uso del sistema.
|-- reservas_main.py       # Archivo principal para ejecutar la aplicación.
|-- reserva_model.py       # Creación de la clase Reserva.


## AUTOR

- **Desarrollador**: Lucas Carasso
- **Email**: lucascarasso007@gmail.com
- **GitHub**: https://github.com/LucasCarasso

---

## VERSIÓN

- **Versión Actual**: 1.0
- **Fecha de Creación**: 12/12/2024

---


**© 2024 Sistema de Reservas de Cabaña**





