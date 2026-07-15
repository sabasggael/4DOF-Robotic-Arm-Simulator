from math import *
import numpy as np
from ClasesVector3D import Vector3D
from ClasesComponentes import Componentes
 
class ArticulacionRotacional(Componentes):
    def __init__(self, nombre, id_componente, longitud, angulo_min, angulo_max, eje_rotacion, radio_colision=0.5, offset_angulo=0.0):
        super().__init__(nombre, id_componente)
        self._longitud = longitud
        self._angulo_min = angulo_min
        self._angulo_max = angulo_max
        self._angulo_actual = 0.0
        self._eje_rotacion = eje_rotacion
        self._radio_colision = radio_colision  # Radio para detección de colisiones
        self._offset_angulo = offset_angulo  # Offset para ajustar posición "cero" real
 
    @property
    def eje_rotacion(self):
        return self._eje_rotacion
    
    @property
    def angulo_actual(self):
        return self._angulo_actual
    
    @property
    def angulo_real(self):
        """Retorna el ángulo real (con offset aplicado) usado en cálculos cinemáticos"""
        return self._angulo_actual + self._offset_angulo
    
    @property
    def radio_colision(self):
        return self._radio_colision
 
    def calcular_matriz_homogenea(self):
        """
        Calcula la matriz de transformación homogénea 4x4 para esta articulación.
        
        Implementa cinemática donde:
        - Base: Rota en plano horizontal (XY)
        - Otras articulaciones: Rotan en plano vertical acumulando ángulos
        
        IMPORTANTE: Usa convención donde ángulos positivos suben el brazo.
        Utiliza el ángulo real (con offset) para los cálculos.
        """
        # Usar ángulo real para cálculos de matrices
        theta = radians(self.angulo_real)
        L = self._longitud
    
        if self._eje_rotacion == 'Z':
            # BASE: Rotación estándar en Z (horizontal)
            return np.array([
                [cos(theta), -sin(theta), 0, L * cos(theta)],
                [sin(theta),  cos(theta), 0, L * sin(theta)],
                [0,           0,          1, 0              ],
                [0,           0,          0, 1              ]
            ])
    
        elif self._eje_rotacion == 'Y':
            # HOMBRO/CODO: Rotación en Y con convención invertida
            # Esta es rotación en Y con signos invertidos respecto a convención estándar
            return np.array([
                [cos(theta),  0, -sin(theta), L * cos(theta)],
                [0,           1,  0,           0             ],
                [sin(theta),  0,  cos(theta), L * sin(theta)],
                [0,           0,  0,           1             ]
            ])
    
        elif self._eje_rotacion == 'X':
            return np.array([
                [cos(theta),  0, -sin(theta), L * cos(theta)],
                [0,           1,  0,           0             ],
                [sin(theta),  0,  cos(theta), L * sin(theta)],
                [0,           0,  0,           1             ]
            ])
 
        else:
            return np.eye(4)
    
    def propiedades(self):
        datos = super().propiedades()
        datos["eje_rotacion"] = self._eje_rotacion
        datos["radio_colision"] = self._radio_colision
        datos["offset_angulo"] = self._offset_angulo
        return datos
    
    def validar(self):
        return self.validar_limites(self._angulo_actual)
    
    def validar_limites(self, angulo):
        return self._angulo_min <= angulo <= self._angulo_max
    
    def mover(self, angulo):
        if self.validar_limites(angulo):
            self._angulo_actual = angulo
            return True
        else:
            print(
                f"Error: Ángulo '{angulo}°' fuera de límites "
                f"({self._angulo_min}°, {self._angulo_max}°)"
            )
            return False
    
    def obtener_info(self):
        return (
            f"{self.nombre}: "
            f"Ángulo={self.angulo_actual}°, "
            f"Límites=[{self._angulo_min}°, {self._angulo_max}°], "
            f"Eje={self._eje_rotacion}, "
            f"Radio={self._radio_colision}"
        )
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco