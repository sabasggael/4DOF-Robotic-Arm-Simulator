from os import system
from Pre_Menu import datos_principal, info_principal
from Menu_s import mostrar_menu_principal, menu_demostraciones
from Info_Sistema import mostrar_info_sistema
from Funciones_Brazo import mover_brazo_menu, mover_brazo_interpolado, mostrar_estado, visualizar_brazo, verificar_seguridad
from Funciones_Config import guardar_configuracion_menu, cargar_configuracion_menu
from Funciones_Secuencia import guardar_secuencia_menu, cargar_secuencia_menu
from ClasesBrazoRobotico import BrazoRobotico
from ClasesGestorArchivos import GestorArchivos
 
def main():
    brazo = BrazoRobotico()
    gestor = GestorArchivos()
    brazo.mover_a_configuracion([0, 0, 0, 0], verificar_colisiones=False)
    datos_principal()
    system("pause")
    system("cls")
    info_principal()
    system("pause")
    system("cls")
 
    while True:
        mostrar_menu_principal()
        try:
            opcion = int(input("\nSeleccione una opción: "))
 
            match opcion:
                case 1:
                    mover_brazo_menu(brazo)
                case 2:
                    mover_brazo_interpolado(brazo)
                case 3:
                    mostrar_estado(brazo)
                case 4:
                    visualizar_brazo(brazo)
                case 5:
                    verificar_seguridad(brazo)
                case 6:
                    guardar_configuracion_menu(brazo, gestor)
                case 7:
                    cargar_configuracion_menu(brazo, gestor)
                case 8:
                    guardar_secuencia_menu(brazo, gestor)
                case 9:
                    cargar_secuencia_menu(brazo, gestor)
                case 10:
                    menu_demostraciones(brazo)
                case 11:
                    mostrar_info_sistema()
                case 12:
                    print("\n¡Gracias por usar el programa!")
                    print("Cerrando sistema...")
                    break
                case _:
                    print("Opción no válida. Intente nuevamente.")
 
            system("pause")
            system("cls")
 
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario")
            break
 
        except Exception as e:
            print(f"\nError inesperado: {e}")
            import traceback
            traceback.print_exc()
            system("pause")
            system("cls")
 
if __name__ == "__main__":
    main()
 
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco