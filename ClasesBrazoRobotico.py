from math import *
import numpy as np
from ClasesVector3D import Vector3D
from ClasesArticulacionRotacional import ArticulacionRotacional
from ClasesConfiguracion import Configuracion
 
class BrazoRobotico:
    def __init__(self):
        # Radios de colisión distintos: base más gruesa, muñeca más delgada
        self.base = ArticulacionRotacional("Base", 1, 2, -180, 180, 'Z', radio_colision=1.0, offset_angulo=0.0)
        # HOMBRO: límites usuario [-70, 70], offset 90° para que 0° sea vertical
        self.hombro = ArticulacionRotacional("Hombro", 2, 10, -70, 70, 'Y', radio_colision=0.8, offset_angulo=90.0)
        self.codo = ArticulacionRotacional("Codo", 3, 8, -135, 135, 'Y', radio_colision=0.6, offset_angulo=0.0)
        self.muñeca = ArticulacionRotacional("Muñeca", 4, 4, -135, 135, 'X', radio_colision=0.4, offset_angulo=0.0)
        self.configuraciones_historial = []  # Lista para almacenar configuraciones guardadas
        self.componentes = [self.base, self.hombro, self.codo, self.muñeca]
 
    def cinematica_directa(self):
        """Devuelve (x, y, z) del efector final usando el método incremental"""
        posiciones = self.obtener_todas_posiciones()
        ultimo = posiciones[-1]
        return (ultimo.x, ultimo.y, ultimo.z)
 
    def cinematica_directa_matrices(self):
        """
        Calcula la posición del efector final usando matrices homogéneas.
        Método más elegante y modular (Denavit-Hartenberg).
        Retorna: (x, y, z)
        """
        # Matriz identidad inicial (sistema de referencia base)
        T = np.eye(4)
 
        # Multiplicar matrices de cada articulación
        for componente in self.componentes:
            T = T @ componente.calcular_matriz_homogenea()
 
        # Extraer posición del efector final (última columna, primeras 3 filas)
        return (T[0, 3], T[1, 3], T[2, 3])
 
    def obtener_todas_posiciones_matrices(self):
        """
        Calcula todas las posiciones de las articulaciones usando matrices homogéneas.
        Retorna: lista de Vector3D [base, hombro, codo, muñeca, efector]
        """
        posiciones = [Vector3D(0, 0, 0)]  # Posición base
        T = np.eye(4)  # Matriz acumulada
 
        for componente in self.componentes:
            T = T @ componente.calcular_matriz_homogenea()
            posiciones.append(Vector3D(T[0, 3], T[1, 3], T[2, 3]))
 
        return posiciones
 
    def mover_a_configuracion(self, angulos, verificar_colisiones=True):
        """
        Intenta mover al vector de ángulos. Primero simula la configuración y verifica colisiones
        (self-collision). Si hay colisión, no aplica el movimiento y devuelve False.
        """
        # Validar límites
        if not all([self.base.validar_limites(angulos[0]),
                    self.hombro.validar_limites(angulos[1]),
                    self.codo.validar_limites(angulos[2]),
                    self.muñeca.validar_limites(angulos[3])]):
            print("Error: Uno o más ángulos fuera de límites.")
            return False
 
        if verificar_colisiones:
            # Simular posiciones para esos ángulos (sin mutar estado)
            posiciones_sim = self.obtener_todas_posiciones_para_angulos(angulos)
 
            # Comprobar colisiones internas con radios distintos
            colisiones = self._detectar_colisiones_entre_posiciones_radios(posiciones_sim)
            if colisiones:
                print("Movimiento rechazado: se detectaron colisiones internas en la simulación:")
                for i, j, d in colisiones:
                    print(f"  - Colisión entre eslabón {i} y {j}, distancia = {d:.3f}")
                return False
 
        # No hay colisiones → aplicar movimiento real
        self.base.mover(angulos[0])
        self.hombro.mover(angulos[1])
        self.codo.mover(angulos[2])
        self.muñeca.mover(angulos[3])
        config = Configuracion(angulos, nombre=f"Config_{len(self.configuraciones_historial)+1}")
        self.configuraciones_historial.append(config)
        return True
 
    def interpolar_trayectoria(self, angulos_destino, num_pasos=20, verificar_colisiones=True):
        """
        Interpola suavemente desde la configuración actual hasta angulos_destino.
        Verifica colisiones en cada paso intermedio para garantizar ruta segura.
        Parámetros:
        - angulos_destino: [θ1, θ2, θ3, θ4] configuración objetivo
        - num_pasos: número de pasos intermedios (mayor = más suave)
        - verificar_colisiones: si True, verifica colisiones en cada paso
        Retorna:
        - (True, trayectoria) si éxito
        - (False, None) si hay colisión en ruta
        """
        # Obtener configuración inicial
        angulos_inicio = [
            self.base.angulo_actual,
            self.hombro.angulo_actual,
            self.codo.angulo_actual,
            self.muñeca.angulo_actual
        ]
 
        # Validar límites del destino
        if not all([self.base.validar_limites(angulos_destino[0]),
                    self.hombro.validar_limites(angulos_destino[1]),
                    self.codo.validar_limites(angulos_destino[2]),
                    self.muñeca.validar_limites(angulos_destino[3])]):
            print("Error: Configuración destino fuera de límites.")
            return (False, None)
 
        # Generar trayectoria interpolada
        trayectoria = []
        for i in range(num_pasos + 1):
            t = i / num_pasos  # Parámetro de interpolación [0, 1]
 
            # Interpolación lineal de ángulos
            angulos_inter = [
                angulos_inicio[j] + t * (angulos_destino[j] - angulos_inicio[j])
                for j in range(4)
            ]
 
            # Verificar colisiones en este punto intermedio
            if verificar_colisiones:
                posiciones_inter = self.obtener_todas_posiciones_para_angulos(angulos_inter)
 
                # Verificar auto-colisiones
                colisiones = self._detectar_colisiones_entre_posiciones_radios(posiciones_inter)
                if colisiones:
                    print(f"Auto-colisión detectada en paso {i}/{num_pasos}:")
                    for idx1, idx2, d in colisiones:
                        print(f"  - Eslabón {idx1} y {idx2}, distancia = {d:.3f}")
                    return (False, None)
 
            trayectoria.append(angulos_inter)
 
        return (True, trayectoria)
 
    def ejecutar_trayectoria_interpolada(self, angulos_destino, num_pasos=20):
        """
        Ejecuta una trayectoria interpolada, moviendo el brazo suavemente.
        Si detecta colisión, se detiene y revierte al estado inicial.
 
        Retorna: True si éxito, False si hubo colisión
        """
        # Guardar estado inicial por si falla
        estado_inicial = [
            self.base.angulo_actual,
            self.hombro.angulo_actual,
            self.codo.angulo_actual,
            self.muñeca.angulo_actual
        ]
 
        exito, trayectoria = self.interpolar_trayectoria(angulos_destino, num_pasos)
 
        if not exito:
            print("Trayectoria rechazada. Manteniendo configuración actual.")
            return False
 
        # Ejecutar trayectoria paso a paso
        print(f"Ejecutando trayectoria interpolada ({num_pasos} pasos)...")
        for i, angulos in enumerate(trayectoria):
            self.base.mover(angulos[0])
            self.hombro.mover(angulos[1])
            self.codo.mover(angulos[2])
            self.muñeca.mover(angulos[3])
 
            # Registrar en historial solo configuraciones clave
            if i % 5 == 0 or i == len(trayectoria) - 1:
                config = Configuracion(angulos, nombre=f"Trayectoria_paso_{i}")
                self.configuraciones_historial.append(config)
 
        print("Trayectoria completada exitosamente")
        return True
 
    def obtener_todas_posiciones(self):
        """Calcula posiciones con los ángulos actuales del brazo (usa el estado)."""
        posiciones = [Vector3D(0, 0, 0)]  # Posición base
        θ1 = radians(self.base.angulo_real)
        θ2 = radians(self.hombro.angulo_real)
        θ3 = radians(self.codo.angulo_real)
        θ4 = radians(self.muñeca.angulo_real)
        l1 = self.base._longitud
        l2 = self.hombro._longitud
        l3 = self.codo._longitud
        l4 = self.muñeca._longitud
        # Posición del hombro
        x1 = l1 * cos(θ1)
        y1 = l1 * sin(θ1)
        z1 = 0
        posiciones.append(Vector3D(x1, y1, z1))
        # Posición del codo
        x2 = x1 + l2 * cos(θ1) * cos(θ2)
        y2 = y1 + l2 * sin(θ1) * cos(θ2)
        z2 = z1 + l2 * sin(θ2)
        posiciones.append(Vector3D(x2, y2, z2))
        # Posición de la muñeca
        x3 = x2 + l3 * cos(θ1) * cos(θ2 + θ3)
        y3 = y2 + l3 * sin(θ1) * cos(θ2 + θ3)
        z3 = z2 + l3 * sin(θ2 + θ3)
        posiciones.append(Vector3D(x3, y3, z3))
        # Posición del efector final
        x4 = x3 + l4 * cos(θ1) * cos(θ2 + θ3 + θ4)
        y4 = y3 + l4 * sin(θ1) * cos(θ2 + θ3 + θ4)
        z4 = z3 + l4 * sin(θ2 + θ3 + θ4)
        posiciones.append(Vector3D(x4, y4, z4))
 
        return posiciones
 
    def obtener_todas_posiciones_para_angulos(self, angulos):
        """Calcula posiciones sin mutar el estado del brazo, para un vector de ángulos dado."""
        # Aplicar offsets a los ángulos para obtener ángulos reales
        θ1 = radians(angulos[0] + self.base._offset_angulo)
        θ2 = radians(angulos[1] + self.hombro._offset_angulo)
        θ3 = radians(angulos[2] + self.codo._offset_angulo)
        θ4 = radians(angulos[3] + self.muñeca._offset_angulo)
 
        l1 = self.base._longitud
        l2 = self.hombro._longitud
        l3 = self.codo._longitud
        l4 = self.muñeca._longitud
 
        posiciones = [Vector3D(0, 0, 0)]
 
        x1 = l1 * cos(θ1)
        y1 = l1 * sin(θ1)
        z1 = 0
        posiciones.append(Vector3D(x1, y1, z1))
 
        x2 = x1 + l2 * cos(θ1) * cos(θ2)
        y2 = y1 + l2 * sin(θ1) * cos(θ2)
        z2 = z1 + l2 * sin(θ2)
        posiciones.append(Vector3D(x2, y2, z2))
 
        x3 = x2 + l3 * cos(θ1) * cos(θ2 + θ3)
        y3 = y2 + l3 * sin(θ1) * cos(θ2 + θ3)
        z3 = z2 + l3 * sin(θ2 + θ3)
        posiciones.append(Vector3D(x3, y3, z3))
 
        x4 = x3 + l4 * cos(θ1) * cos(θ2 + θ3 + θ4)
        y4 = y3 + l4 * sin(θ1) * cos(θ2 + θ3 + θ4)
        z4 = z3 + l4 * sin(θ2 + θ3 + θ4)
        posiciones.append(Vector3D(x4, y4, z4))
 
        return posiciones
 
    def calcular_alcance_maximo(self):
        return self.base._longitud + self.hombro._longitud + self.codo._longitud + self.muñeca._longitud
 
    def validar_configuracion(self):
        return all([self.base.validar(), self.hombro.validar(), self.codo.validar(), self.muñeca.validar()])
 
    def obtener_estado(self):
        return {
            "base": self.base.propiedades(),
            "hombro": self.hombro.propiedades(),
            "codo": self.codo.propiedades(),
            "muñeca": self.muñeca.propiedades(),
            "posicion_extremo": self.cinematica_directa(),
            "configuracion_valida": self.validar_configuracion()
        }
 
    @staticmethod
    def _dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z
 
    @staticmethod
    def _segment_segment_distance(p1, q1, p2, q2):
        """
        Distancia mínima entre dos segmentos 3D [p1,q1] y [p2,q2].
        Implementación basada en algoritmo geométrico estándar.
        p1,q1,p2,q2: Vector3D
        Retorna: distancia (float)
        """
        # vector u = q1 - p1
        u = Vector3D(q1.x - p1.x, q1.y - p1.y, q1.z - p1.z)
        # vector v = q2 - p2
        v = Vector3D(q2.x - p2.x, q2.y - p2.y, q2.z - p2.z)
        # w0 = p1 - p2
        w0 = Vector3D(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)
        a = BrazoRobotico._dot(u, u)
        b = BrazoRobotico._dot(u, v)
        c = BrazoRobotico._dot(v, v)
        d = BrazoRobotico._dot(u, w0)
        e = BrazoRobotico._dot(v, w0)
        D = a * c - b * b
        sc, sN, sD = 0.0, 0.0, D
        tc, tN, tD = 0.0, 0.0, D
        SMALL_NUM = 1e-9
 
        if D < SMALL_NUM:
            sN = 0.0
            sD = 1.0
            tN = e
            tD = c
        else:
            sN = (b * e - c * d)
            tN = (a * e - b * d)
            if sN < 0.0:
                sN = 0.0
            elif sN > sD:
                sN = sD
 
        if tN < 0.0:
            tN = 0.0
            if -d < 0.0:
                sN = 0.0
            elif -d > a:
                sN = sD
            else:
                sN = -d
                sD = a
        elif tN > tD:
            tN = tD
            if (-d + b) < 0.0:
                sN = 0
            elif (-d + b) > a:
                sN = sD
            else:
                sN = (-d + b)
                sD = a
 
        sc = 0.0 if abs(sN) < SMALL_NUM else sN / sD
        tc = 0.0 if abs(tN) < SMALL_NUM else tN / tD
 
        # dP = w0 + sc*u - tc*v
        dP = Vector3D(w0.x + (sc * u.x) - (tc * v.x),
                      w0.y + (sc * u.y) - (tc * v.y),
                      w0.z + (sc * u.z) - (tc * v.z))
        return dP.magnitud()
 
    def _detectar_colisiones_entre_posiciones_radios(self, posiciones):
        segmentos = []
        radios = []
 
        for i in range(len(posiciones)-1):
            segmentos.append((posiciones[i], posiciones[i+1]))
            radios.append(self.componentes[i].radio_colision)
 
        colisiones = []
        n = len(segmentos)
 
        for i in range(n):
            for j in range(i+1, n):
                # Ignorar segmentos adyacentes
                if j == i + 1:
                    continue
 
                p1, q1 = segmentos[i]
                p2, q2 = segmentos[j]
                dist = self._segment_segment_distance(p1, q1, p2, q2)
 
                # Suma de radios de ambos segmentos
                radio_sum = radios[i] + radios[j]
 
                if dist < radio_sum:
                    colisiones.append((i, j, dist))
 
        return colisiones
 
    def detectar_colisiones_self_mejorado(self):
        """Usa radios distintos y el estado actual del brazo."""
        posiciones = self.obtener_todas_posiciones()
        return self._detectar_colisiones_entre_posiciones_radios(posiciones)
 
    def verificar_seguridad_total(self):
        """
        Verifica todas las condiciones de seguridad:
        - Límites angulares
        - Auto-colisiones
 
        Retorna: (seguro: bool, problemas: list)
        """
        problemas = []
 
        # Verificar límites
        if not self.validar_configuracion():
            problemas.append("Ángulos fuera de límites")
 
        # Verificar auto-colisiones
        colisiones = self.detectar_colisiones_self_mejorado()
        if colisiones:
            problemas.append(f"Auto-colisiones detectadas: {len(colisiones)}")
 
        return (len(problemas) == 0, problemas)
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco