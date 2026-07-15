from abc import ABC, abstractmethod
 
class Componentes(ABC):
    def __init__(self, nombre, id_componente):
        self.nombre = nombre
        self.id_componente = id_componente
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
 
    @property
    def longitud(self):
        return self._longitud
    
    @abstractmethod
    def propiedades(self):
        return {
            "nombre": self.nombre,
            "id": self.id_componente
        }
    
    @abstractmethod
    def validar(self):
        pass
 
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco