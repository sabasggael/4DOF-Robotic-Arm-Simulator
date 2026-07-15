import csv
import json
import os
from datetime import datetime
from ClasesConfiguracion import Configuracion
 
class GestorArchivos:
    def __init__(self, ruta_base="./datos_robot/"):
        self.ruta_base = ruta_base
        os.makedirs(self.ruta_base, exist_ok=True)
 
    # ========== CONFIGURACIONES INDIVIDUALES ==========
    
    def guardar_configuracion_json(self, configuracion, nombre_archivo="configuracion.json"):
        """Guarda una configuración individual en JSON"""
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            with open(ruta_completa, mode='w') as archivo_json:
                json.dump(configuracion.a_diccionario(), archivo_json, indent=4)
            print(f"Configuración guardada en '{ruta_completa}'")
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")
    
    def cargar_configuracion_json(self, nombre_archivo="configuracion.json"):
        """Carga una configuración individual desde JSON"""
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            with open(ruta_completa, mode='r') as archivo_json:
                datos = json.load(archivo_json)
                configuracion = Configuracion.desde_diccionario(datos)
            print(f"Configuración cargada desde '{ruta_completa}'")
            return configuracion
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
            return None
    
    def guardar_configuracion_csv(self, configuracion, nombre_archivo="configuracion.csv"):
        """
        Guarda una configuración individual en CSV.
        Formato: nombre,theta1,theta2,theta3,theta4,fecha_creacion
        """
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            with open(ruta_completa, mode='w', newline='') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                # Encabezados
                escritor.writerow(['nombre', 'theta1', 'theta2', 'theta3', 'theta4', 'fecha_creacion'])
                # Datos
                escritor.writerow([
                    configuracion.nombre,
                    configuracion.angulos[0],
                    configuracion.angulos[1],
                    configuracion.angulos[2],
                    configuracion.angulos[3],
                    configuracion.fecha_creacion.isoformat()
                ])
            print(f"Configuración guardada en '{ruta_completa}'")
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")
    
    def cargar_configuracion_csv(self, nombre_archivo="configuracion.csv"):
        """Carga una configuración individual desde CSV"""
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            with open(ruta_completa, mode='r', newline='') as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                fila = next(lector)  # Leer primera fila
                
                angulos = [
                    float(fila['theta1']),
                    float(fila['theta2']),
                    float(fila['theta3']),
                    float(fila['theta4'])
                ]
                
                config = Configuracion(angulos, nombre=fila['nombre'])
                
                # Parsear fecha si existe
                if 'fecha_creacion' in fila and fila['fecha_creacion']:
                    try:
                        config.fecha_creacion = datetime.fromisoformat(fila['fecha_creacion'])
                    except:
                        config.fecha_creacion = datetime.now()
                
                print(f"Configuración cargada desde '{ruta_completa}'")
                return config
                
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
            return None
    
    # ========== SECUENCIAS DE CONFIGURACIONES ==========
    
    def guardar_secuencia_json(self, lista_configuraciones, nombre_archivo="secuencia.json"):
        """
        Guarda una secuencia completa de configuraciones en JSON.
        Permite reproducir movimientos complejos.
        """
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            secuencia = {
                "nombre": nombre_archivo.replace('.json', ''),
                "fecha_creacion": datetime.now().isoformat(),
                "num_pasos": len(lista_configuraciones),
                "configuraciones": [config.a_diccionario() for config in lista_configuraciones]
            }
            
            with open(ruta_completa, mode='w') as archivo_json:
                json.dump(secuencia, archivo_json, indent=2)
            
            print(f"Secuencia guardada en '{ruta_completa}'")
            print(f"  • {len(lista_configuraciones)} configuraciones")
        except Exception as e:
            print(f"Error al guardar la secuencia: {e}")
    
    def cargar_secuencia_json(self, nombre_archivo="secuencia.json"):
        """Carga una secuencia de configuraciones desde JSON"""
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            with open(ruta_completa, mode='r') as archivo_json:
                datos = json.load(archivo_json)
            
            configuraciones = [
                Configuracion.desde_diccionario(config_dict) 
                for config_dict in datos["configuraciones"]
            ]
            
            print(f"Secuencia cargada desde '{ruta_completa}'")
            print(f"  • {len(configuraciones)} configuraciones")
            print(f"  • Creada: {datos.get('fecha_creacion', 'Desconocida')}")
            
            return configuraciones
        except Exception as e:
            print(f"Error al cargar la secuencia: {e}")
            return None
    
    def guardar_secuencia_csv(self, lista_configuraciones, nombre_archivo="secuencia.csv"):
        """
        Guarda una secuencia de configuraciones en CSV.
        Formato: paso,nombre,theta1,theta2,theta3,theta4,fecha_creacion
        
        Ideal para:
        - Edición en Excel/Google Sheets
        - Análisis de datos
        - Secuencias largas (más ligero que JSON)
        """
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            with open(ruta_completa, mode='w', newline='') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                
                # Encabezados
                escritor.writerow(['paso', 'nombre', 'theta1', 'theta2', 'theta3', 'theta4', 'fecha_creacion'])
                
                # Escribir cada configuración
                for i, config in enumerate(lista_configuraciones, start=1):
                    escritor.writerow([
                        i,
                        config.nombre,
                        config.angulos[0],
                        config.angulos[1],
                        config.angulos[2],
                        config.angulos[3],
                        config.fecha_creacion.isoformat()
                    ])
            
            print(f"Secuencia guardada en '{ruta_completa}'")
            print(f"  • {len(lista_configuraciones)} pasos")
            print(f"  • Formato CSV (editable en Excel)")
        except Exception as e:
            print(f"Error al guardar la secuencia: {e}")
    
    def cargar_secuencia_csv(self, nombre_archivo="secuencia.csv"):
        """Carga una secuencia de configuraciones desde CSV"""
        ruta_completa = os.path.join(self.ruta_base, nombre_archivo)
        try:
            configuraciones = []
            
            with open(ruta_completa, mode='r', newline='') as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                
                for fila in lector:
                    try:
                        angulos = [
                            float(fila['theta1']),
                            float(fila['theta2']),
                            float(fila['theta3']),
                            float(fila['theta4'])
                        ]
                        
                        config = Configuracion(angulos, nombre=fila.get('nombre', f"Paso_{fila.get('paso', '?')}"))
                        
                        # Parsear fecha
                        if 'fecha_creacion' in fila and fila['fecha_creacion']:
                            try:
                                config.fecha_creacion = datetime.fromisoformat(fila['fecha_creacion'])
                            except:
                                config.fecha_creacion = datetime.now()
                        
                        configuraciones.append(config)
                        
                    except Exception as e:
                        print(f"Advertencia: Error en paso {fila.get('paso', '?')}: {e}")
                        continue
            
            print(f"Secuencia cargada desde '{ruta_completa}'")
            print(f"  • {len(configuraciones)} configuraciones")
            
            return configuraciones if configuraciones else None
            
        except Exception as e:
            print(f"Error al cargar la secuencia: {e}")
            return None
    
    # ========== UTILIDADES ==========
        
    def listar_archivos(self, extension=".csv"):
        """Lista archivos con una extensión específica"""
        try:
            archivos = [f for f in os.listdir(self.ruta_base) if f.endswith(extension)]
            if archivos:
                print(f"\nArchivos con extensión '{extension}' en '{self.ruta_base}':")
                for i, archivo in enumerate(archivos, 1):
                    print(f"  {i}. {archivo}")
            else:
                print(f"No hay archivos con extensión '{extension}' en '{self.ruta_base}'")
            return archivos
        except Exception as e:
            print(f"Error al listar archivos: {e}")
            return []
 
# Sabas Garduño Gael
# Fundamentos de Programación
# ESIME Zacatenco