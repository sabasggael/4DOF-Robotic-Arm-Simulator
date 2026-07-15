import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 - necesario para registrar la proyección 3D
import numpy as np
from ClasesVector3D import Vector3D
 
class Visualizador3D:
    def __init__(self):
        self.fig = None
        self.ax = None
 
    def configurar_escena(self, titulo = "Visualización 3D del Brazo Robótico"):
        self.fig = plt.figure(figsize=(12, 9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        limite = 25
        self.ax.set_xlim([-limite, limite])
        self.ax.set_ylim([-limite, limite])
        self.ax.set_zlim([0, limite])
        self.ax.set_xlabel('Eje X')
        self.ax.set_ylabel('Eje Y')
        self.ax.set_zlabel('Eje Z')
        self.ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20, color='navy', loc='center')
        self.ax.grid(True, alpha=0.3)
 
    def dibujar_brazo(self, brazo, color_eslabones='blue', color_articulaciones='red'):
        posiciones = brazo.obtener_todas_posiciones()
        xs = [pos.x for pos in posiciones]
        ys = [pos.y for pos in posiciones]
        zs = [pos.z for pos in posiciones]
        self.ax.plot(xs, ys, zs, color=color_eslabones, linewidth=3, marker='o', markerfacecolor=color_articulaciones, markersize=8, markeredgecolor='black', markeredgewidth=2, label='Estructura del Brazo')
        self.ax.scatter([0], [0], [0], color='green', s=200, marker='^', label='Base del Brazo', edgecolor='black', linewidths=2)
        self.ax.scatter([xs[-1]], [ys[-1]], [zs[-1]], color='orange', s=200, marker='*', label='Extremo del Brazo', edgecolors='black', linewidths=2)
        self.ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
 
    def dibujar_vectores(self, brazo, escala=1.0, color_vector='purple'):
        posiciones = brazo.obtener_todas_posiciones()
        for i in range(len(posiciones)-1):
            inicio = posiciones[i]
            fin = posiciones[i+1]
            dx = fin.x - inicio.x
            dy = fin.y - inicio.y  
            dz = fin.z - inicio.z
            self.ax.quiver(inicio.x, inicio.y, inicio.z, dx, dy, dz, length=escala, color=color_vector, arrow_length_ratio=0.1, linewidth=1.5, alpha=0.7)
 
    def dibujar_trayectoria(self, lista_posiciones, color='cyan'):
        if len(lista_posiciones) < 2:
            return
        xs = [p[0] for p in lista_posiciones]
        ys = [p[1] for p in lista_posiciones]
        zs = [p[2] for p in lista_posiciones]
        self.ax.plot(xs, ys, zs, color=color, linewidth=2, alpha=0.6, linestyle='--', label='Trayectoria del Extremo')
    
    def dibujar_espacio_trabajo(self, radio_maximo, color='lightgray', alpha=0.3):
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        x = radio_maximo * np.outer(np.cos(u), np.sin(v))
        y = radio_maximo * np.outer(np.sin(u), np.sin(v))
        z = radio_maximo * np.outer(np.ones(np.size(u)), np.cos(v))
        z = np.abs(z)
        self.ax.plot_surface(x, y, z, alpha = 0.1, color='gray', edgecolor='none')
 
    def agregar_sistema_coordenadas(self, origen=Vector3D(0,0,0), longitud=5):
        self.ax.quiver(origen.x, origen.y, origen.z, longitud, 0, 0, color='red', arrow_length_ratio=0.2, linewidth=2, label='Eje X')
        self.ax.quiver(origen.x, origen.y, origen.z, 0, longitud, 0, color='green', arrow_length_ratio=0.2, linewidth=2, label='Eje Y')
        self.ax.quiver(origen.x, origen.y, origen.z, 0, 0, longitud, color='blue', arrow_length_ratio=0.2, linewidth=2, label='Eje Z')
 
    def mostrar(self, guardar_imagen=False, nombre_archivo="visualizacion_brazo.png"):
        self.ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
        if guardar_imagen:
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
            print(f"Imagen guardada como '{nombre_archivo}'")
        plt.show()
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco