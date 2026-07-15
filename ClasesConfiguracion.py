from datetime import datetime
 
class Configuracion:
    def __init__(self, angulos, nombre = "Sin nombre"):
        self.angulos = angulos  # [θ1, θ2, θ3, θ4]
        self.nombre = nombre
        self.fecha_creacion = datetime.now()
 
    def a_diccionario(self):
        return {
            "nombre": self.nombre,
            "angulos": self.angulos,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }
    
    @staticmethod
    def desde_diccionario(datos):
        config = Configuracion(angulos = datos["angulos"], nombre = datos.get("nombre", "Sin nombre"))
        # Parsear fecha si viene
        if "fecha_creacion" in datos:
            try:
                config.fecha_creacion = datetime.fromisoformat(datos["fecha_creacion"])
            except Exception:
                config.fecha_creacion = datetime.now()
        return config
    
    def __str__(self):
        fecha = self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if hasattr(self, "fecha_creacion") else "Sin fecha"
        return f"Configuración '{self.nombre}': Angulos = [θ1={self.angulos[0]}°, θ2={self.angulos[1]}°, θ3={self.angulos[2]}°, θ4={self.angulos[3]}°], Creada el {fecha}"
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco