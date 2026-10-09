import pandas as pd
from sqlalchemy import create_engine
import os
import time

class ValidadorEInsertador:
    def __init__(self, user, password, host, db_name):
        cadena_conexion = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
        self.engine = create_engine(cadena_conexion)
        self.ruta_csv = "csv_congreso"
        
        self.reglas = {
            'INST': ['ITZ', 'UNAM', 'UAEM', 'UTEZ', 'UPMOR', 'IPN'],
            'TIPO_PART': ['E', 'P'],
            'COSTOS_CONF': [100.00, 155.00, 210.00],
            'COSTOS_TALLER': [250.00, 300.00, 450.00],
            'GRADOS': ['ING', 'LIC', 'MC', 'DR', 'DRA', 'MTI']
        }
        
        # Diccionario para almacenar los DataFrames en memoria
        self.dfs = {}

    def cargar_y_validar(self):
        print("--- FASE 1: CARGA Y VALIDACIÓN DE REGLAS DE NEGOCIO ---")
        
        # 1. PARTICIPANTE
        df = pd.read_csv(os.path.join(self.ruta_csv, 'participante.csv'))
        filas_ini = len(df)
        df = df[df['INST'].isin(self.reglas['INST']) & df['TIPO_PART'].isin(self.reglas['TIPO_PART'])]
        print(f"PARTICIPANTE: {len(df)} filas válidas (Descartadas: {filas_ini - len(df)})")
        self.dfs['PARTICIPANTE'] = df

        # 2. TALLER
        df = pd.read_csv(os.path.join(self.ruta_csv, 'taller.csv'))
        filas_ini = len(df)
        df['FECHA_INI'] = pd.to_datetime(df['FECHA_INI'])
        df['FECHA_FIN'] = pd.to_datetime(df['FECHA_FIN'])
        # Validar costo y lógica de fechas (Fin >= Inicio)
        df = df[df['COSTO'].isin(self.reglas['COSTOS_TALLER']) & (df['FECHA_FIN'] >= df['FECHA_INI'])]
        print(f"TALLER: {len(df)} filas válidas (Descartadas por costo ridículo o fecha ilógica: {filas_ini - len(df)})")
        self.dfs['TALLER'] = df

        # 3. ARTICULOS
        self.dfs['ARTICULOS'] = pd.read_csv(os.path.join(self.ruta_csv, 'articulos.csv'))
        print(f"ARTICULOS: {len(self.dfs['ARTICULOS'])} filas válidas")

        # 4. AUTORES
        df = pd.read_csv(os.path.join(self.ruta_csv, 'autores.csv'))
        filas_ini = len(df)
        df = df[df['GRADO'].isin(self.reglas['GRADOS'])]
        print(f"AUTORES: {len(df)} filas válidas (Descartadas: {filas_ini - len(df)})")
        self.dfs['AUTORES'] = df

        # 5. CONFERENCIA (Regla 1:1 y Costos)
        df = pd.read_csv(os.path.join(self.ruta_csv, 'conferencia.csv'))
        filas_ini = len(df)
        # Validar costos y que no haya artículos duplicados (Regla 1:1)
        df = df[df['COSTO'].isin(self.reglas['COSTOS_CONF'])]
        df = df.drop_duplicates(subset=['ARTICULOS_CLAVE_ART']) 
        print(f"CONFERENCIA: {len(df)} filas válidas (Descartadas: {filas_ini - len(df)})")
        self.dfs['CONFERENCIA'] = df

        # 6. INSTRUCTOR
        df = pd.read_csv(os.path.join(self.ruta_csv, 'instructor.csv'))
        filas_ini = len(df)
        df = df[df['INSTITUCION'].isin(self.reglas['INST']) & df['GRADO'].isin(self.reglas['GRADOS'])]
        print(f"INSTRUCTOR: {len(df)} filas válidas (Descartadas: {filas_ini - len(df)})")
        self.dfs['INSTRUCTOR'] = df

    def validar_integridad_referencial(self):
        print("\n--- FASE 2: VALIDACIÓN DE INTEGRIDAD REFERENCIAL (LLAVES COMPUESTAS) ---")
        
        # 7. PARTICIPANTE_CONFERENCIA
        df = pd.read_csv(os.path.join(self.ruta_csv, 'participante_conferencia.csv'))
        filas_ini = len(df)
        df = df.drop_duplicates()
        df = df[df['CONFERENCIA_CLAVE_CONF'].isin(self.dfs['CONFERENCIA']['CLAVE_CONF'])]
        df = df[df['PARTICIPANTE_CLAVE_PART'].isin(self.dfs['PARTICIPANTE']['CLAVE_PART'])]
        print(f"PARTICIPANTE_CONFERENCIA: {len(df)} filas congruentes (Descartadas: {filas_ini - len(df)})")
        self.dfs['PARTICIPANTE_CONFERENCIA'] = df

        # 8. PARTICIPANTE_TALLER
        df = pd.read_csv(os.path.join(self.ruta_csv, 'participante_taller.csv'))
        filas_ini = len(df)
        df = df.drop_duplicates()
        df = df[df['PARTICIPANTE_CLAVE_PART'].isin(self.dfs['PARTICIPANTE']['CLAVE_PART'])]
        df = df[df['TALLER_CLAVE INT'].isin(self.dfs['TALLER']['CLAVE INT'])]
        print(f"PARTICIPANTE_TALLER: {len(df)} filas congruentes (Descartadas: {filas_ini - len(df)})")
        self.dfs['PARTICIPANTE_TALLER'] = df

        # 9. AUTORES_ARTICULOS
        df = pd.read_csv(os.path.join(self.ruta_csv, 'autores_articulos.csv'))
        filas_ini = len(df)
        df = df.drop_duplicates()
        df = df[df['AUTORES_idAutor'].isin(self.dfs['AUTORES']['idAutor'])]
        df = df[df['ARTICULOS_CLAVE_ART'].isin(self.dfs['ARTICULOS']['CLAVE_ART'])]
        print(f"AUTORES_ARTICULOS: {len(df)} filas congruentes (Descartadas: {filas_ini - len(df)})")
        self.dfs['AUTORES_ARTICULOS'] = df

    def insertar_en_mysql(self):
        print("\n--- FASE 3: INSERCIÓN EN MYSQL (TRANSACCIÓN SEGURA) ---")
        orden_insercion = [
            'PARTICIPANTE', 'TALLER', 'ARTICULOS', 'AUTORES',
            'CONFERENCIA', 'INSTRUCTOR',
            'PARTICIPANTE_CONFERENCIA', 'PARTICIPANTE_TALLER', 'AUTORES_ARTICULOS'
        ]

        print("Iniciando modo transacción: 'Todo o Nada'...")
        
        try:
            # engine.begin() abre la transacción. Si hay un error, hace ROLLBACK automático.
            # Si termina el bloque 'with' sin errores, hace COMMIT automático.
            with self.engine.begin() as connection:
                for tabla in orden_insercion:
                    df = self.dfs[tabla]
                    if df.empty:
                        print(f"Advertencia: No hay datos para la tabla {tabla}.")
                        continue
                    
                    print(f"Validando y encolando {len(df)} registros para {tabla}...")
                    start_time = time.time()
                    
                    # Mandamos la conexión transaccional (connection) en lugar del engine
                    df.to_sql(name=tabla.lower(), con=connection, if_exists='append', index=False, chunksize=10000, method='multi')
                    
                    tiempo = time.time() - start_time
                    print(f"✓ {tabla} encolada exitosamente en {tiempo:.2f} segundos.")
                
                print("\nTodas las tablas pasaron los filtros de MySQL.")
                
            # Si el código llega a esta línea, la transacción fue un éxito.
            print("\n¡Proceso terminado!")

        except Exception as e:
            # Si MySQL rechaza cualquier dato (ej. un Varchar muy largo o llave duplicada), 
            # entra a este bloque y deshace TODO lo que se había encolado.
            print("\n" + "="*60)
            print("❌ ALERTA CRÍTICA: MYSQL RECHAZÓ LOS DATOS")
            print("Se detectó un error de integridad. Se ha ejecutado un ROLLBACK.")
            print("Ningún dato fue insertado. Tu base de datos sigue intacta.")
            print("="*60)
            print(f"Detalle del error:\n{e}")

if __name__ == "__main__":
    usuario_mysql = "root"
    password_mysql = "root" 
    host_mysql = "127.0.0.1"
    base_datos = "Congreso"

    etl = ValidadorEInsertador(usuario_mysql, password_mysql, host_mysql, base_datos)
    
    # Previo a correr esto, asegúrate de haber vaciado las tablas con el TRUNCATE que vimos
    etl.cargar_y_validar()
    etl.validar_integridad_referencial()
    etl.insertar_en_mysql()