from ClasesConfiguracion import Configuracion
 
def guardar_configuracion_menu(brazo, gestor):
    """Guarda configuración actual en JSON o CSV"""
    print("\n--- GUARDAR CONFIGURACIÓN ---")
    print("Seleccione formato:")
    print("1. JSON (estructura completa)")
    print("2. CSV (editable en Excel)")
    
    try:
        formato = int(input("Opción: "))
        
        nombre = input("Nombre de la configuración: ")
        nombre_base = input("Nombre del archivo (sin extensión): ")
        
        config = Configuracion(
            [brazo.base.angulo_actual, 
             brazo.hombro.angulo_actual, 
             brazo.codo.angulo_actual,
             brazo.muñeca.angulo_actual],
            nombre
        )
        
        if formato == 1:
            gestor.guardar_configuracion_json(config, nombre_base + ".json")
        elif formato == 2:
            gestor.guardar_configuracion_csv(config, nombre_base + ".csv")
        else:
            print("Opción inválida")
    except ValueError:
        print("Error: Ingrese un número válido")
 
def cargar_configuracion_menu(brazo, gestor):
    """Carga configuración desde JSON o CSV"""
    print("\n--- CARGAR CONFIGURACIÓN ---")
    print("Seleccione formato:")
    print("1. JSON")
    print("2. CSV")
    
    try:
        formato = int(input("Opción: "))
        
        if formato == 1:
            archivos = gestor.listar_archivos(".json")
            if not archivos:
                return
            
            opcion = int(input("\nSeleccione archivo (número): "))
            if 1 <= opcion <= len(archivos):
                config = gestor.cargar_configuracion_json(archivos[opcion - 1])
                if config:
                    brazo.mover_a_configuracion(config.angulos)
                    print(f"Configuración '{config.nombre}' aplicada al brazo")
        
        elif formato == 2:
            archivos = gestor.listar_archivos(".csv")
            if not archivos:
                return
            
            opcion = int(input("\nSeleccione archivo (número): "))
            if 1 <= opcion <= len(archivos):
                config = gestor.cargar_configuracion_csv(archivos[opcion - 1])
                if config:
                    brazo.mover_a_configuracion(config.angulos)
                    print(f"Configuración '{config.nombre}' aplicada al brazo")
        
        else:
            print("Opción inválida")
            
    except ValueError:
        print("Error: Ingrese un número válido")
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco