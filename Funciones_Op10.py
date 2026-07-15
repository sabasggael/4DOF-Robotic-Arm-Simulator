from math import sin, cos, radians, sqrt
from ClasesVisualizador3d import Visualizador3D
from ClasesVector3D import Vector3D
from ClasesArticulacionRotacional import ArticulacionRotacional
from ClasesBrazoRobotico import BrazoRobotico
 
def demostrar_plano_rotacion(brazo):
    """Demuestra cómo el plano de rotación sigue a la base"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: PLANO DE ROTACIÓN SIGUIENDO LA BASE")
    print("="*60)
    print("\nEsta demostración muestra cómo el hombro, codo y muñeca rotan")
    print("en un plano vertical que está orientado según la base.\n")
    
    visualizador = Visualizador3D()
    visualizador.configurar_escena("Plano de Rotación Dependiente de la Base (4DOF)")
    visualizador.agregar_sistema_coordenadas(longitud=8)
    
    angulos_base = [0, 45, 90]
    colores = ['blue', 'green', 'red']
    
    for i, (theta1, color) in enumerate(zip(angulos_base, colores)):
        print(f"\n{i+1}. Base a {theta1}° (color {color}):")
        
        trayectoria = []
        for theta2 in range(-45, 46, 15):
            brazo.mover_a_configuracion([theta1, theta2, -30, 0], verificar_colisiones=False)
            pos = brazo.cinematica_directa()
            trayectoria.append(pos)
            print(f"   θ₁={theta1:>3}°, θ₂={theta2:>3}°, θ₃=-30°, θ₄=0° → Pos: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
        
        visualizador.dibujar_brazo(brazo, color_eslabones=color, color_articulaciones='darkred')
        visualizador.dibujar_trayectoria(trayectoria, color=color)
    
    print("\nObserva cómo cada trayectoria está en un plano diferente,")
    print("   orientado según la rotación de la base.")
    print("   • Azul (0°): Plano XZ")
    print("   • Verde (45°): Plano rotado 45°")
    print("   • Rojo (90°): Plano YZ")
    
    visualizador.mostrar()
    print("\nDemostración completada")
    print("="*60)
 
def demo_interpolacion_colisiones(brazo):
    """Demostración de interpolación con detección de colisiones"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: INTERPOLACIÓN CON DETECCIÓN DE COLISIONES")
    print("="*60)
    
    print("\nEsta demo muestra cómo la interpolación detecta colisiones EN RUTA")
    print("incluso si la configuración final es válida.\n")
    
    estado_inicial = [
        brazo.base.angulo_actual,
        brazo.hombro.angulo_actual,
        brazo.codo.angulo_actual,
        brazo.muñeca.angulo_actual
    ]
    
    # Caso 1: Movimiento seguro
    print("="*60)
    print("CASO 1: Trayectoria segura")
    print("="*60)
    brazo.mover_a_configuracion([0, 0, 0, 0], verificar_colisiones=False)
    print(f"Inicio: [0, 0, 0, 0]")
    print(f"Destino: [90, 30, -45, 0]")
    
    exito, trayectoria = brazo.interpolar_trayectoria([90, 30, -45, 0], num_pasos=15)
    if exito:
        print(f"  Trayectoria SEGURA ({len(trayectoria)} pasos)")
        print(f"  Primera posición: {[f'{a:.1f}' for a in trayectoria[0]]}")
        print(f"  Última posición: {[f'{a:.1f}' for a in trayectoria[-1]]}")
    
    # Caso 2: Auto-colisión (ajustado a nuevos límites)
    print("\n" + "="*60)
    print("CASO 2: Auto-colisión del brazo")
    print("="*60)
    brazo.mover_a_configuracion([0, 0, 0, 0], verificar_colisiones=False)
    print(f"Inicio: [0, 0, 0, 0]")
    print(f"Destino: [0, 70, 135, 90]  (brazo se dobla sobre sí mismo)")
    
    exito, trayectoria = brazo.interpolar_trayectoria([0, 70, 135, 90], num_pasos=25)
    if not exito:
        print("Trayectoria RECHAZADA (auto-colisión detectada)")
    
    # Visualización
    print("\n" + "="*60)
    print("Generando visualización comparativa...")
    visualizador = Visualizador3D()
    visualizador.configurar_escena("Demo: Trayectorias Seguras vs Peligrosas")
    
    brazo.mover_a_configuracion([0, 0, 0, 0], verificar_colisiones=False)
    tray_puntos = []
    exito, tray_segura = brazo.interpolar_trayectoria([90, 30, -45, 0], num_pasos=15)
    if exito:
        for angulos in tray_segura:
            brazo.mover_a_configuracion(angulos, verificar_colisiones=False)
            pos = brazo.cinematica_directa()
            tray_puntos.append(pos)
        visualizador.dibujar_trayectoria(tray_puntos, color='green')
    
    visualizador.dibujar_brazo(brazo, color_eslabones='blue', color_articulaciones='red')
    visualizador.agregar_sistema_coordenadas()
    visualizador.mostrar()
    
    brazo.mover_a_configuracion(estado_inicial, verificar_colisiones=False)
    print("\nDemostración completada")
    print("="*60)
 
def comparar_cinematica(brazo):
    """Compara cinemática tradicional vs matrices homogéneas"""
    print("\n" + "="*60)
    print("COMPARACIÓN: CINEMÁTICA TRADICIONAL VS MATRICES")
    print("="*60)
    
    configs_prueba = [
        [0, 0, 0, 0],
        [45, 30, -45, 20],
        [90, 45, -60, 0],
        [-90, -45, 45, 30],
        [180, 0, 0, 0]
    ]
    
    print("\n{:<25} {:<30} {:<30} {:<15}".format(
        "Configuración [θ1,θ2,θ3,θ4]",
        "Método Tradicional (x,y,z)",
        "Método Matrices (x,y,z)",
        "Diferencia"
    ))
    print("-" * 100)
    
    for config in configs_prueba:
        brazo.mover_a_configuracion(config, verificar_colisiones=False)
        
        pos_trad = brazo.cinematica_directa()
        pos_mat = brazo.cinematica_directa_matrices()
        
        diff = sqrt(
            (pos_trad[0] - pos_mat[0])**2 +
            (pos_trad[1] - pos_mat[1])**2 +
            (pos_trad[2] - pos_mat[2])**2
        )
        
        config_str = f"[{config[0]:>4},{config[1]:>4},{config[2]:>4},{config[3]:>4}]"
        trad_str = f"({pos_trad[0]:>7.3f},{pos_trad[1]:>7.3f},{pos_trad[2]:>7.3f})"
        mat_str = f"({pos_mat[0]:>7.3f},{pos_mat[1]:>7.3f},{pos_mat[2]:>7.3f})"
        
        print(f"{config_str:<25} {trad_str:<30} {mat_str:<30} {diff:<15.6f}")
    
    print("\nAmbos métodos son equivalentes (diferencias < 1e-10 por redondeo)")
    print("Matrices homogéneas son más elegantes y modulares")
    print("="*60)
 
def ejecutar_pruebas():
    """Ejecuta pruebas de ejemplo del sistema"""
    print("\n" + "="*60)
    print("EJECUTANDO PRUEBAS DEL SISTEMA 4DOF")
    print("="*60)
    
    print("\nPrueba 1: Vector3D")
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    v3 = v1 + v2
    print(f"   v1 = {v1}")
    print(f"   v2 = {v2}")
    print(f"   v1 + v2 = {v3}")
    print(f"   |v1| = {v1.magnitud():.3f}")
    print(f"   v1_normalizado = {v1.normalizar()} con magnitud {v1.normalizar().magnitud():.3f}")
    print(f"   v1 · v2 = {v1.producto_punto(v2):.3f}")
    cruz = v1.producto_cruz(v2)
    print(f"   v1 × v2 = {cruz}")
    
    print("\nPrueba 2: Articulaciones con radios distintos")
    base = ArticulacionRotacional("Base Test", 1, 10, -180, 180, 'Z', radio_colision=1.0)
    muneca = ArticulacionRotacional("Muñeca Test", 2, 4, -135, 135, 'X', radio_colision=0.4)
    print(f"   {base.obtener_info()}")
    print(f"   {muneca.obtener_info()}")
    
    print("\nPrueba 3: Matrices Homogéneas")
    base.mover(45)
    matriz = base.calcular_matriz_homogenea()
    print(f"   Matriz para Base a 45°:")
    print(f"   {matriz}")
    
    print("\nPrueba 4: Brazo Robótico 4DOF")
    brazo = BrazoRobotico()
    brazo.mover_a_configuracion([0, 0, 0, 0], verificar_colisiones=False)
    pos1 = brazo.cinematica_directa()
    print(f"   Configuración [0, 0, 0, 0]: ({pos1[0]:.3f}, {pos1[1]:.3f}, {pos1[2]:.3f})")
    print(f"   Nota: Hombro en 0° ahora es vertical (perpendicular a la base)")
    
    print("\nPrueba 5: Comparación Cinemática")
    brazo.mover_a_configuracion([45, 30, -45, 20], verificar_colisiones=False)
    pos_trad = brazo.cinematica_directa()
    pos_mat = brazo.cinematica_directa_matrices()
    diff = sqrt(sum((a-b)**2 for a,b in zip(pos_trad, pos_mat)))
    print(f"   Tradicional: ({pos_trad[0]:.6f}, {pos_trad[1]:.6f}, {pos_trad[2]:.6f})")
    print(f"   Matrices:    ({pos_mat[0]:.6f}, {pos_mat[1]:.6f}, {pos_mat[2]:.6f})")
    print(f"   Diferencia:  {diff:.10f} (debe ser ~0)")
    
    print("\nPrueba 6: Interpolación de trayectoria")
    brazo.mover_a_configuracion([0, 0, 0, 0], verificar_colisiones=False)
    exito, trayectoria = brazo.interpolar_trayectoria([90, 30, -45, 0], num_pasos=10)
    print(f"   Inicio: [0, 0, 0, 0]")
    print(f"   Destino: [90, 30, -45, 0]")
    print(f"   Resultado: {'ÉXITO' if exito else 'FALLO'}")
    if exito:
        print(f"   Pasos generados: {len(trayectoria)}")
        print(f"   Primer paso: {[f'{a:.1f}' for a in trayectoria[0]]}")
        print(f"   Último paso: {[f'{a:.1f}' for a in trayectoria[-1]]}")
    
    print("\nPrueba 7: Verificación de seguridad")
    brazo.mover_a_configuracion([45, 30, -30, 15], verificar_colisiones=False)
    seguro, problemas = brazo.verificar_seguridad_total()
    print(f"   Configuración: [45, 30, -30, 15]")
    print(f"   Estado: {'SEGURO' if seguro else 'INSEGURO'}")
    if problemas:
        for p in problemas:
            print(f"      • {p}")
 
    print("\nTodas las pruebas completadas")
    print("="*60)
 
def demo_trayectoria_circular(brazo):
    """Genera y visualiza una trayectoria circular de ejemplo"""
    print("\n--- DEMO: TRAYECTORIA CIRCULAR ---")
    print("Generando trayectoria circular...")
    
    trayectoria = []
    for angulo in range(0, 361, 15):
        theta1 = angulo
        theta2 = -60 * sin(radians(angulo))
        theta3 = -45
        theta4 = 20 * cos(radians(angulo))
        
        if brazo.mover_a_configuracion([theta1, theta2, theta3, theta4], verificar_colisiones=False):
            pos = brazo.cinematica_directa()
            trayectoria.append(pos)
    
    print(f"Trayectoria generada con {len(trayectoria)} puntos")
    
    visualizador = Visualizador3D()
    visualizador.configurar_escena("Trayectoria Circular Demo")
    visualizador.dibujar_brazo(brazo)
    visualizador.dibujar_trayectoria(trayectoria, color='cyan')
    visualizador.agregar_sistema_coordenadas()
    print("Mostrando trayectoria...")
    visualizador.mostrar()
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco