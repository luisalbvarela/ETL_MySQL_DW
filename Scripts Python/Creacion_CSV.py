import csv
import random
import datetime
import os

carpeta_salida = "csv_congreso"
os.makedirs(carpeta_salida, exist_ok=True)

instituciones = ['ITZ', 'UNAM', 'UAEM', 'UTEZ', 'UPMOR', 'IPN']
tipos_part = ['E', 'P']
costos_conf = [100.00, 155.00, 210.00]
costos_taller = [250.00, 300.00, 450.00]
grados = ['ING', 'LIC', 'MC', 'DR', 'DRA', 'MTI']

nombres = [
    "Carlos", "Maria", "Jorge", "Ana", "Luis", "Elena", "Fernando", "Lucia",
    "Gael", "Sofia", "Diego", "Valeria", "Alejandro", "Daniela", "Hugo",
    "Carmen", "Roberto", "Laura", "Miguel", "Patricia", "Jesus", "Martha",
    "Jose", "Andrea", "Manuel", "Teresa", "Ricardo", "Adriana", "Raul", "Rosa",
    "Pedro", "Monica", "Victor", "Silvia", "Eduardo", "Gabriela", "Javier",
    "Natalia", "Francisco", "Claudia", "Antonio", "Diana", "Julio", "Veronica",
    "Oscar", "Beatriz", "Ruben", "Leticia", "Arturo", "Susana", "Rumualdo",
    "Esteban", "Paola", "Rafael", "Carolina", "Martin", "Lorena", "Gerardo",
    "Margarita", "Hector"
]

apellidos = [
    "Garcia", "Martinez", "Lopez", "Gonzalez", "Perez", "Rodriguez", "Sanchez",
    "Ramirez", "Cruz", "Gomez", "Flores", "Morales", "Ortiz", "Gutierrez",
    "Ruiz", "Hernandez", "Diaz", "Reyes", "Aguilar", "Mendoza", "Castillo",
    "Chavez", "Romero", "Herrera", "Medina", "Dominguez", "Castro", "Vargas",
    "Guzman", "Velazquez", "Rojas", "Mendez", "Munoz", "Salazar", "Garza",
    "Soto", "Navarro", "Delgado", "Vega", "Rios", "Avila", "Ramos", "Campos",
    "Escobar", "Valencia", "Silva", "Cordova", "Paredes", "Sosa", "Molina",
    "Bautista", "Cortes", "Espinoza", "Lara", "Cabrera", "Maldonado",
    "Cervantes", "Mejia"
]

temas = [
    "Bases de Datos", "Redes Neuronales", "Ciberseguridad", "Cloud Computing",
    "Sistemas Embebidos", "IoT y Domotica", "DevOps", "Robotica Industrial",
    "Machine Learning", "Big Data", "Redes Fisicas", "Cableado Estructurado",
    "Enrutamiento", "Pipelines ETL", "Optimizacion SQL", "Vision Artificial",
    "Seguridad Industrial", "Riesgos Industriales con IA",
    "Algoritmos Predictivos", "Modelos Probabilisticos", "Analisis Estadistico",
    "Backtesting de Algoritmos", "Software Seguro", "Blockchain",
    "Realidad Aumentada", "Ingenieria de Software", "Microservicios",
    "Criptografia", "Computacion Cuantica", "Automatizacion de Pruebas",
    "Diseno de APIs REST", "Contenedores Docker", "SO Distribuidos",
    "Mineria de Datos", "Business Intelligence", "Telemetria",
    "Sistemas de Control", "Desarrollo Movil", "Edge Computing",
    "Lenguaje Natural (NLP)"
]

# --- VOLÚMENES ---
NUM_PART = 15000
NUM_TALLERES = 3000
NUM_ARTICULOS = 11000
NUM_AUTORES = 3000
NUM_CONF = 10500
NUM_INST = 3000
TARGET_PC = 500000  # OBJETIVO DE REGISTROS


def random_date():
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2026, 4, 30)
    dias_totales = (end - start).days
    return start + datetime.timedelta(days=random.randint(0, dias_totales))


def write_csv(filename, headers, data):
    filepath = os.path.join(carpeta_salida, filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Generado: {filename} ({len(data)} filas)")


# 1. Creacion de participantes
datos_part = [[i, random.choice(nombres), random.choice(apellidos),
               random.choice(apellidos), random.choice(instituciones),
               random.choice(tipos_part), 'Mexicana',
               f'Dir {random.randint(1, 1000)}']
              for i in range(1, NUM_PART + 1)]
write_csv('participante.csv',
          ['CLAVE_PART', 'NOM', 'AP_PAT', 'AP_MAT', 'INST', 'TIPO_PART',
           'NACIONALIDAD', 'DIR'], datos_part)

# 2. Creacion de talleres
datos_taller = []
for i in range(1, NUM_TALLERES + 1):
    f_ini = random_date()
    # Para la fecha fin, sumamos entre 1 y 3 días a la fecha de inicio
    datos_taller.append([i, f'Taller: {random.choice(temas)}',
                         random.choice(costos_taller), f_ini,
                         f_ini + datetime.timedelta(days=random.randint(1, 3))])
write_csv('taller.csv',
          ['CLAVE INT', 'NOMBRE', 'COSTO', 'FECHA_INI', 'FECHA_FIN'],
          datos_taller)

# 3. Creacion de articulos
datos_art = [[i, f'Art. {i}: {random.choice(temas)}']
             for i in range(1, NUM_ARTICULOS + 1)]
write_csv('articulos.csv', ['CLAVE_ART', 'TITULO'], datos_art)

# 4. Creacion de autores
datos_aut = [[i, f"{random.choice(nombres)} {random.choice(apellidos)}",
              f"autor{i}@mail.com", random.choice(grados)]
             for i in range(1, NUM_AUTORES + 1)]
write_csv('autores.csv', ['idAutor', 'NOMBRE', 'CORREO', 'GRADO'], datos_aut)

# 5. Creacion de conferencias
articulos_disp = random.sample(range(1, NUM_ARTICULOS + 1), NUM_CONF)
datos_conf = [[i, random.choice(costos_conf), random_date(), articulos_disp[i - 1]]
              for i in range(1, NUM_CONF + 1)]
write_csv('conferencia.csv',
          ['CLAVE_CONF', 'COSTO', 'FECHA', 'ARTICULOS_CLAVE_ART'], datos_conf)

# 6. Creacion de instructores
datos_inst = [[i, f"{random.choice(nombres)} {random.choice(apellidos)}",
               random.choice(instituciones), random.choice(grados),
               random.randint(1, NUM_TALLERES)]
              for i in range(1, NUM_INST + 1)]
write_csv('instructor.csv',
          ['idInstructor', 'NOM', 'INSTITUCION', 'GRADO', 'TALLER_CLAVE INT'],
          datos_inst)

# 7. Balanceo de 500 mil registros
print("Calculando asignaciones de conferencias (Objetivo exacto: 500,000 registros)...")

# Generamos capacidad máxima de asistentes por conferencia
capacidades_conf = [random.randint(35, 60) for _ in range(NUM_CONF)]
total_actual = sum(capacidades_conf)

while total_actual < TARGET_PC:
    idx = random.randint(0, NUM_CONF - 1)
    if capacidades_conf[idx] < 60:
        capacidades_conf[idx] += 1
        total_actual += 1

while total_actual > TARGET_PC:
    idx = random.randint(0, NUM_CONF - 1)
    if capacidades_conf[idx] > 35:
        capacidades_conf[idx] -= 1
        total_actual -= 1

# 8. Creacion de la tabla PARTICIPANTE_CONFERENCIA
datos_pc = []
for conf_id in range(1, NUM_CONF + 1):
    cupo_asignado = capacidades_conf[conf_id - 1]
    asistentes = random.sample(range(1, NUM_PART + 1), cupo_asignado)
    for part_id in asistentes:
        datos_pc.append([conf_id, part_id])

write_csv('participante_conferencia.csv',
          ['CONFERENCIA_CLAVE_CONF', 'PARTICIPANTE_CLAVE_PART'], datos_pc)

# 9. Creacion de la tabla PARTICIPANTE_TALLER
datos_pt = []
for taller_id in range(1, NUM_TALLERES + 1):
    cupo_taller = random.randint(35, 60)
    asistentes = random.sample(range(1, NUM_PART + 1), cupo_taller)
    for part_id in asistentes:
        datos_pt.append([part_id, taller_id])

write_csv('participante_taller.csv',
          ['PARTICIPANTE_CLAVE_PART', 'TALLER_CLAVE INT'], datos_pt)


# 10. Creacion de AUTORES_ARTICULOS
def generar_pares(max_a, max_b, total):
    pares = set()
    while len(pares) < total:
        pares.add((random.randint(1, max_a), random.randint(1, max_b)))
    return list(pares)


NUM_AA = 6000
write_csv('autores_articulos.csv',
          ['AUTORES_idAutor', 'ARTICULOS_CLAVE_ART'],
          generar_pares(NUM_AUTORES, NUM_ARTICULOS, NUM_AA))

print("\n¡Proceso terminado!")