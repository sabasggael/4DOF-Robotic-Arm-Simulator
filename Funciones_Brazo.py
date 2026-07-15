from ClasesVisualizador3d import Visualizador3D
 
def mover_brazo_menu(brazo):
    """Submenú para mover el brazo"""
    print("\n--- MOVER BRAZO ---")
    print(f"Límites:")
    print(f"  • Base: [-180°, 180°]")
    print(f"  • Hombro: [-70°, 70°]  (0° = vertical)")
    print(f"  • Codo: [-135°, 135°]")
    print(f"  • Muñeca: [-135°, 135°]")
    
    try:
        theta1 = float(input("Ingrese ángulo Base (θ₁): "))
        theta2 = float(input("Ingrese ángulo Hombro (θ₂): "))
        theta3 = float(input("Ingrese ángulo Codo (θ₃): "))
        theta4 = float(input("Ingrese ángulo Muñeca (θ₄): "))
        
        if brazo.mover_a_configuracion([theta1, theta2, theta3, theta4]):
            pos = brazo.cinematica_directa()
            print(f"\nMovimiento exitoso")
            print(f"Posición del efector final: ({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})")
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
 
def mover_brazo_interpolado(brazo):
    """Mueve el brazo con interpolación suave"""
    print("\n--- MOVER CON INTERPOLACIÓN SUAVE ---")
    print("Este modo genera una trayectoria suave y verifica colisiones en ruta")
    print(f"\nConfiguración actual:")
    print(f"  Base={brazo.base.angulo_actual:.1f}°, Hombro={brazo.hombro.angulo_actual:.1f}°")
    print(f"  Codo={brazo.codo.angulo_actual:.1f}°, Muñeca={brazo.muñeca.angulo_actual:.1f}°")
    
    try:
        theta1 = float(input("\nIngrese ángulo Base destino (θ₁): "))
        theta2 = float(input("Ingrese ángulo Hombro destino (θ₂): "))
        theta3 = float(input("Ingrese ángulo Codo destino (θ₃): "))
        theta4 = float(input("Ingrese ángulo Muñeca destino (θ₄): "))
        
        num_pasos = int(input("Número de pasos de interpolación (10-50, recomendado 20): ") or "20")
        
        print(f"\nInterpolando trayectoria con {num_pasos} pasos...")
        if brazo.ejecutar_trayectoria_interpolada([theta1, theta2, theta3, theta4], num_pasos):
            pos = brazo.cinematica_directa()
            print(f"Posición final: ({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})")
        else:
            print("Movimiento no realizado")
            
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
 
def verificar_seguridad(brazo):
    """Verifica todas las condiciones de seguridad"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE SEGURIDAD TOTAL")
    print("="*60)
    
    seguro, problemas = brazo.verificar_seguridad_total()
    
    print("\nConfiguración actual:")
    print(f"  Base: {brazo.base.angulo_actual:.1f}° (radio: {brazo.base.radio_colision})")
    print(f"  Hombro: {brazo.hombro.angulo_actual:.1f}° (radio: {brazo.hombro.radio_colision})")
    print(f"  Codo: {brazo.codo.angulo_actual:.1f}° (radio: {brazo.codo.radio_colision})")
    print(f"  Muñeca: {brazo.muñeca.angulo_actual:.1f}° (radio: {brazo.muñeca.radio_colision})")
    
    pos = brazo.cinematica_directa()
    print(f"\nPosición efector: ({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})")
    
    print("\n--- RESULTADOS DE SEGURIDAD ---")
    if seguro:
        print("ESTADO: SEGURO")
        print("  • Todos los límites respetados")
        print("  • Sin auto-colisiones")
    else:
        print("ESTADO: INSEGURO")
        print("Problemas detectados:")
        for problema in problemas:
            print(f"  • {problema}")
    
    colisiones = brazo.detectar_colisiones_self_mejorado()
    if colisiones:
        print(f"\nColisiones detectadas: {len(colisiones)}")
        for i, j, d in colisiones:
            print(f"  • Eslabón {i} ↔ Eslabón {j}: distancia {d:.3f}")
    print("="*60)
 
def mostrar_estado(brazo):
    """Muestra estado completo del brazo"""
    print("\n--- ESTADO ACTUAL DEL BRAZO ---")
    estado = brazo.obtener_estado()
    print(f"\nBase: {brazo.base.obtener_info()}")
    print(f"Hombro: {brazo.hombro.obtener_info()}")
    print(f"Codo: {brazo.codo.obtener_info()}")
    print(f"Muñeca: {brazo.muñeca.obtener_info()}")
    
    pos = estado['posicion_extremo']
    print(f"\nEfector Final: ({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})")
    print(f"Configuración válida: {'Sí' if estado['configuracion_valida'] else 'No'}")
    print(f"Alcance máximo: {brazo.calcular_alcance_maximo():.2f} unidades")
    print(f"Configuraciones en historial: {len(brazo.configuraciones_historial)}")
    
    seguro, problemas = brazo.verificar_seguridad_total()
    if seguro:
        print(f"Estado de seguridad: SEGURO")
    else:
        print(f"Estado de seguridad: INSEGURO")
        for problema in problemas:
            print(f"   • {problema}")
 
def visualizar_brazo(brazo):
    """Visualiza el brazo en 3D"""
    print("\n--- VISUALIZACIÓN 3D ---")
    visualizador = Visualizador3D()
    visualizador.configurar_escena("Configuración Actual del Brazo 4DOF")
    visualizador.agregar_sistema_coordenadas()
    visualizador.dibujar_brazo(brazo)
    visualizador.dibujar_vectores(brazo)
    visualizador.dibujar_espacio_trabajo(brazo.calcular_alcance_maximo())
    print("Mostrando visualización 3D...")
    visualizador.mostrar()
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco