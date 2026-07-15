from ClasesVisualizador3d import Visualizador3D

def guardar_secuencia_menu(brazo, gestor):
    """Guarda el historial de configuraciones como secuencia en JSON o CSV"""
    print("\n--- GUARDAR SECUENCIA DE MOVIMIENTOS ---")
    
    if not brazo.configuraciones_historial:
        print("No hay configuraciones en el historial para guardar")
        return
    
    print(f"Configuraciones en historial: {len(brazo.configuraciones_historial)}")
    print("\nSeleccione formato:")
    print("1. JSON (estructura completa)")
    print("2. CSV (editable en Excel, ideal para análisis)")
    
    try:
        formato = int(input("Opción: "))
        nombre_base = input("Nombre del archivo (sin extensión): ")
        
        if formato == 1:
            gestor.guardar_secuencia_json(brazo.configuraciones_historial, nombre_base + ".json")
        elif formato == 2:
            gestor.guardar_secuencia_csv(brazo.configuraciones_historial, nombre_base + ".csv")
        else:
            print("Opción inválida")
    except ValueError:
        print("Error: Ingrese un número válido")

def cargar_secuencia_menu(brazo, gestor):
    """Carga y ejecuta una secuencia de configuraciones desde JSON o CSV"""
    print("\n--- CARGAR Y EJECUTAR SECUENCIA ---")
    print("Seleccione formato:")
    print("1. JSON")
    print("2. CSV")
    
    try:
        formato = int(input("Opción: "))
        secuencia = None
        
        if formato == 1:
            archivos = gestor.listar_archivos(".json")
            if not archivos:
                return
            
            opcion = int(input("\nSeleccione archivo (número): "))
            if 1 <= opcion <= len(archivos):
                secuencia = gestor.cargar_secuencia_json(archivos[opcion - 1])
        
        elif formato == 2:
            archivos = gestor.listar_archivos(".csv")
            if not archivos:
                return
            
            opcion = int(input("\nSeleccione archivo (número): "))
            if 1 <= opcion <= len(archivos):
                secuencia = gestor.cargar_secuencia_csv(archivos[opcion - 1])
        
        else:
            print("Opción inválida")
            return
        
        # Si se cargó correctamente la secuencia, ejecutar
        if secuencia:
            print("\nOpciones de ejecución:")
            print("1. Ejecutar secuencia completa (automático)")
            print("2. Ejecutar paso a paso (manual)")
            print("3. Solo visualizar trayectoria")
            
            modo = int(input("Seleccione modo: "))
            
            if modo == 1:
                # Ejecución automática
                print("\nEjecutando secuencia...")
                for i, config in enumerate(secuencia):
                    if brazo.mover_a_configuracion(config.angulos):
                        print(f"  Paso {i+1}/{len(secuencia)}: {config.nombre}")
                    else:
                        print(f"  Error en paso {i+1}, deteniendo ejecución")
                        break
                print("✓ Secuencia completada")
            
            elif modo == 2:
                # Paso a paso
                for i, config in enumerate(secuencia):
                    print(f"\nPaso {i+1}/{len(secuencia)}: {config.nombre}")
                    print(f"Ángulos: [{config.angulos[0]:.1f}, {config.angulos[1]:.1f}, {config.angulos[2]:.1f}, {config.angulos[3]:.1f}]")
                    input("Presione Enter para continuar...")
                    brazo.mover_a_configuracion(config.angulos)
            
            elif modo == 3:
                # Solo visualizar
                print("\nGenerando visualización...")
                visualizador = Visualizador3D()
                visualizador.configurar_escena("Secuencia Cargada")
                
                # Generar trayectoria
                trayectoria = []
                for config in secuencia:
                    brazo.mover_a_configuracion(config.angulos, verificar_colisiones=False)
                    pos = brazo.cinematica_directa()
                    trayectoria.append(pos)
                
                visualizador.dibujar_brazo(brazo)
                visualizador.dibujar_trayectoria(trayectoria, color='cyan')
                visualizador.agregar_sistema_coordenadas()
                visualizador.mostrar()
            
            else:
                print("Opción inválida")
                
    except ValueError:
        print("Error: Ingrese un número válido")

# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco