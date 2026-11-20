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
        #  Linea que crea un cliente de prueba
        cliente1 = Cliente(1, "Elier Lorenzo Estrella Rz", "1086925057")
        
        # Funcion que imprimir los datos del cliente
        print(cliente1.mostrar_datos()) 

        logging.info(f"Cliente creado exitosamente: {cliente1.mostrar_datos()}")
        
    except AttributeError as e:
        # Funcion que identifica si hay algun error llamando a los metodos.
        print(f"Error detectado en el codigo: {e}")
        logging.error(f"Fallo de atributo: {e}")
        
    except Exception as e:
        # Funcion que notifica el error general.
        print(f"Error general: {e}")
        logging.error(f"Error general: {e}")

    finally:
            
        print("Finalisando el primer avance del cliete.") 

if __name__ == "__main__":
    main()