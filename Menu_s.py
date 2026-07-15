from os import system
from Funciones_Op10 import (
    demostrar_plano_rotacion,
    demo_interpolacion_colisiones,
    comparar_cinematica,
    ejecutar_pruebas,
    demo_trayectoria_circular
)
 
def mostrar_menu_principal():
    system("color 7F")
    print("\n" + "="*102)
    print("                    S I M U L A D O R  D E  B R A Z O  R O B Ó T I C O  4 D O F")
    print("="*102)
    print('''
1. Mover brazo a configuración específica               7. Cargar configuración (JSON/CSV)
2. Mover con interpolación suave                        8. Guardar secuencia de movimientos (JSON/CSV)
3. Mostrar estado actual del brazo                      9. Cargar y ejecutar secuencia (JSON/CSV)
4. Visualizar brazo en 3D                               10. Demostraciones y pruebas
5. Verificar seguridad total del brazo                  11. Mostrar información del sistema
6. Guardar configuración actual (JSON/CSV)              12. Salir
''')
    print("="*102)
 
def mostrar_menu_demostraciones():
    print("\n" + "="*60)
    print("D E M O S T R A C I O N E S  Y  P R U E B A S")
    print("="*60)
    print("1. Plano de rotación siguiendo la base")
    print("2. Interpolación con detección de colisiones")
    print("3. Comparar cinemática (Tradicional vs Matrices)")
    print("4. Ejecutar pruebas del sistema")
    print("5. Trayectoria circular de ejemplo")
    print("0. Volver al menú principal")
    print("="*60)
 
def menu_demostraciones(brazo):
    """Submenú de demostraciones"""
    while True:
        mostrar_menu_demostraciones()
        try:
            opcion = int(input("\nSeleccione una opción: "))
            
            match opcion:
                case 1:
                    demostrar_plano_rotacion(brazo)
                case 2:
                    demo_interpolacion_colisiones(brazo)
                case 3:
                    comparar_cinematica(brazo)
                case 4:
                    ejecutar_pruebas()
                case 5:
                    demo_trayectoria_circular(brazo)
                case 0:
                    return
                case _:
                    print("Opción no válida")
            
            system("pause")
            system("cls")
            
        except ValueError:
            print("Error: Ingrese un número válido")
            system("pause")
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco