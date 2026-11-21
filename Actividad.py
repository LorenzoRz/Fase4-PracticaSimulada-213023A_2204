# Elier Lorenzo Estrella
# Avance Actividad

from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    filename='registro.log', level=logging.INFO, format='%(asctime)s - %(message)s'
)


# Funcuion para las validaciones 
class ErrorPersonalizado(Exception):
    pass

class ErrorReserva(ErrorPersonalizado):
    pass

# Clase principal
class Entidad(ABC):
    def __init__(self, id_entidad):
        if id_entidad <= 0:
            raise ErrorPersonalizado("El ID de la entidad debe ser un número positivo.")    
        self._id_entidad = id_entidad
        
    @abstractmethod
    def mostrar_datos(self):
        pass

class Cliente(Entidad):
    def __init__(self, id_entidad, nombre, doc):
        super().__init__(id_entidad)
        if not nombre or not doc:
            raise ErrorPersonalizado("El nombre y el documento no pueden estar vacíos.")
        # Datos del Usuario
        self.__nombre = nombre
        self.__doc = doc

    @property
    def nombre(self):
        return self.__nombre
        
    def mostrar_datos(self):
        return f"ID: {self._id_entidad} | Nombre: {self.__nombre} | CC: {self.__doc}"

class Servicio(Entidad):
    def __init__(self, id_entidad, nombre, tarifa):
        super().__init__(id_entidad)
        if tarifa <= 0:
            raise ErrorPersonalizado("La tarifa del servicio debe ser un número positivo.")
        self._nombre = nombre
        self._tarifa = tarifa
        self.disponible = True  # Atributo para indicar si el servicio está disponible

    @abstractmethod
    def validar(self, duracion):
        pass

    @property
    def nombre(self):
        return self._nombre

    def calcular_costo(self, duracion, descuento=0, iva=False):
        self.validar(duracion)
        costo_base = (self._tarifa * duracion) * (1 - descuento)
        return costo_base * 1.19 if iva else costo_base
        
class Sala(Servicio):
    def validar(self, duracion):
        if duracion < 1:
            raise ErrorPersonalizado("La duración debe ser mínimo una hora.")
        
    def mostrar_datos(self):
        return f"Sala: {self._nombre} | Tarifa: ${self._tarifa}/h | Disponible: {self.disponible}"

class Equipo(Servicio):
    def validar(self, duracion):
        if duracion < 1:
            raise ErrorPersonalizado("El equipo se alquila mínimo 1 día.")

    def mostrar_datos(self):
        return f"Equipo: {self._nombre} | Tarifa: ${self._tarifa}/día | Disponible: {self.disponible}"

class Asesoria(Servicio):
    def validar(self, duracion):
        if duracion < 2:
            raise ErrorPersonalizado("La asesoría requiere mínimo 2 horas.")

    def mostrar_datos(self):
        return f"Asesoría: {self._nombre} | Tarifa: ${self._tarifa}/h | Disponible: {self.disponible}"

# Clase Reserva que integra Cliente y Servicio
class Reserva(Entidad):
    def __init__(self, id_entidad, cliente, servicio, duracion):
        super().__init__(id_entidad)
        if not servicio.disponible:
            raise ErrorReserva(f"El servicio '{servicio.nombre}' no está disponible.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.total = 0

    def confirmar(self, descuento=0, iva=False):
        try:
            self.total = self.servicio.calcular_costo(self.duracion, descuento, iva)
        except ErrorPersonalizado as e:
            # Encadenamiento de excepciones.
            raise ErrorReserva("Error al procesar el costo de la reserva.") from e
        self.estado = "CONFIRMADA"
        self.servicio.disponible = False

    def cancelar(self):
        self.estado = "CANCELADA"
        self.servicio.disponible = True

    def mostrar_datos(self):
        return f"Reserva #{self._id_entidad} [{self.estado}] | {self.cliente.nombre} -> {self.servicio.nombre} | Total: ${self.total}"

def main():
    print("Iniciando sitema") 
    clientes=[]
    servicios=[]
    reservas=[]

    try:
        #  Creacion de un cliente de prueba
        cliente1 = Cliente(1, "Elier Lorenzo Estrella Rz", "1086925057")
    except ErrorPersonalizado as e:
        print(f"Error al crear el cliente: {e}")
    else:
        # Funcion que imprimir los datos del cliente
        print(cliente1.mostrar_datos()) 
        logging.info(f"Cliente creado exitosamente: {cliente1.mostrar_datos()}")


    try:
        #  Creacion de un cliente de prueba
        cliente2 = Cliente(2, "Oscar Martinez Ortiz", "98195248")
    except ErrorPersonalizado as e:
        print(f"Error al crear el cliente: {e}")
    else:
        # Funcion que imprimir los datos del cliente
        print(cliente2.mostrar_datos()) 
        logging.info(f"Cliente creado exitosamente: {cliente2.mostrar_datos()}")


    try:
        #  Creacion de un cliente erroneo prueba
        cliente_erronero = Cliente(3, "Brenda", "")
        clientes.append(cliente_erronero)
    except ErrorPersonalizado as e:
        print(f"Error al crear el cliente: {e}")
        logging.error(f"Error en el cliente: {e}")


    try:
        # Linea que crea un servicio de prueba
        sala1 = Sala(1, "Sala de Conferencias", 150000)
    except ErrorPersonalizado as e:
        print(f"Error al crear el servicio: {e}")
    else:
        # Funcion que imprimir los datos del servicio
        print(sala1.mostrar_datos()) 
        logging.info(f"Servicio creado exitosamente: {sala1.mostrar_datos()}")  
    
    try:
        equipo1 = Equipo(2, "Televisor", 500000)
        asesoria1 = Asesoria(3, "Asesoría Legal", 200000)
        servicios.extend([equipo1, asesoria1])
        print(equipo1.mostrar_datos(),"|",asesoria1.mostrar_datos())
        logging.info(f"Servicios creados exitosamente: {equipo1.mostrar_datos()} | {asesoria1.mostrar_datos()}")
    except ErrorPersonalizado as e:
        print(f"Error al crear los servicios: {e}")
        logging.error(f"Error en los servicios: {e}")
#asta aqui probar errorres



    try:
        # Servicio de prueba erroneo
        servicio_invalido = Sala(4, "Sala Inválida", -50)
        servicios.append(servicio_invalido)
    except ErrorPersonalizado as e:
        print(f"Error al crear el servicio: {e}")
        logging.error(f"Error en el servicio: {e}")

    try:
        # Linea que confirma la reserva de prueba
       reserva1 = Reserva(1, cliente1, sala1, 3)
       reserva1.confirmar(descuento=0.1, iva=True)
       reservas.append(reserva1)
       print(reserva1.mostrar_datos())
       logging.info(f"Reserva confirmada exitosamente: {reserva1.mostrar_datos()}")
    except ErrorReserva as e:
        print(f"Error al confirmar la reserva: {e}")
        logging.error(f"Error en la reserva: {e}")
    
    try:
        # Reserva de prueba erronea
        reserva_invalida = Reserva(2, cliente2, sala1, 2)  # Intentando reservar una sala ya reservada
        reserva_invalida.confirmar()
        reservas.append(reserva_invalida)
    except ErrorReserva as e:
        print(f"Error al confirmar la reserva: {e}")
        logging.error(f"Error en la reserva: {e}")

    try:
        # Intentando crear una reserva con un servicio no disponible
        reserva_invalida2 = Reserva(3, cliente2, equipo1, 0)
        reserva_invalida2.confirmar()
        reservas.append(reserva_invalida2)
    except ErrorReserva as e:
        print(f"Error encadenamiento de reservas: {e}")
        logging.error(f"Error en la reserva: {e}")


    except Exception as e:
        # Funcion que notifica el error general.
        print(f"Error general: {e}")
        logging.error(f"Error general: {e}")
        
    finally:
            
        print("Finalisando el primer avance del cliete.") 

if __name__ == "__main__":
    main()