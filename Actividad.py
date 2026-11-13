# Elier Lorenzo Estrella
# Avance Actividad

from abc import ABC, abstractmethod
import logging

logging.basicConfig(filename='registro.log', level=logging.ERROR, 
                    format='%(asctime)s - %(message)s')

# Funcuion para las validaciones 
class ErrorPersonalizado(Exception):
    pass

# Clase principal
class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad
        
    @abstractmethod
    def mostrar_datos(self):
        pass

class Cliente(Entidad):
    def __init__(self, id_entidad, nombre, doc):
        super().__init__(id_entidad)
        # Datos del Usuario
        self.__nombre = nombre
        self.__doc = doc
        
    def mostrar_datos(self):
        return f"ID: {self._id_entidad} | Nombre: {self.__nombre} | CC: {self.__doc}"

def main():
    print("Iniciando sitema") 
    
    try:
        #  Linea que crea un cliente de prueba
        cliente1 = Cliente(1, "Elier Lorenzo Estrella Rz", "1086925057")
        
        # Funcion que imprimir los datos del cliente
        print(cliente1.mostrar_datos()) 
        
    except AttributeError as e:
        # Funcion que identifica si hay algun error llamando a los metodos
        print(f"Error detectado en el codigo: {e}")
        logging.error("Fallo de atributo: {e}")
        
    except Exception as e:
        # Funcion que notifica el error general.
        print("Error general: {e}")
        
    finally:
        print("Finalisando el primer avance del cliete.") 

if __name__ == "__main__":
    main()