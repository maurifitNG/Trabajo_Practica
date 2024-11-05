import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine

# Configuración de conexión a PostgreSQL
db_user = 'user'
db_password = 'password'
db_host = 'localhost'
db_port = '5432'
db_name = 'boletasdb'
table_name = 'boletas'

# Crear la conexión a la base de datos
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Directorio base
path = r'C:\Users\mauri\OneDrive\Escritorio\Portafolio\pruebas'
subdirs = [x[0] for x in os.walk(path)]

appended_data = []

# Procesar cada subdirectorio
for subdir in subdirs:
    # Consigue todos los archivos .txt en el subdirectorio
    files = glob.glob(os.path.join(subdir, "*.txt"))
    for filename in files:
        try:
            # Leer archivo .txt
            data = pd.read_csv(filename, sep=";", header=None, encoding='latin1')
            data = data.iloc[[0], [3, 4, 6, 7, 9, 10, 11, 13, 14, 15, 16, 27, 29, 30]]
            data = data.dropna(axis=1)
            data.columns = ['folio', 'fecha', 'rut_razon_emisor', 'nombre_razon_emisor', 'na', 'direccion', 'comuna', 'neto', 'iva', 'bruto']

            # Obtener el nombre del archivo .ted correspondiente y extraer MNT
            nombre_ted = os.path.splitext(filename)[0] + '.ted'
            mnt_ted = 0
            with open(nombre_ted, 'r', encoding='ISO-8859-1') as file:
                contenido_ted = file.read()
                try:
                    root = ET.fromstring(contenido_ted)
                    valor_MNT = root.find("./DD/MNT").text
                    mnt_ted = float(valor_MNT)
                except ET.ParseError:
                    print(f"Error al analizar el archivo: {filename}")

            # Añadir columnas 'cruce ted', 'descuento' y 'nombre_local'
            data['cruce_ted'] = mnt_ted
            data['descuento'] = data['bruto'].astype(float) - mnt_ted
            data['nombre_local'] = os.path.basename(subdir)

            # Agregar el DataFrame procesado a la lista
            appended_data.append(data)

        except pd.errors.EmptyDataError:
            print(f"El archivo {filename} está vacío. Saltando...")
        except Exception as e:
            print(f'Error en archivo {filename}: {e}')

# Concatenar todos los DataFrames
if appended_data:
    final_data = pd.concat(appended_data, ignore_index=True)

    # Guardar los datos en la base de datos
    try:
        final_data.to_sql(table_name, engine, if_exists='append', index=False)
        print("Datos insertados en la base de datos correctamente.")
    except Exception as e:
        print(f"Error al insertar datos en la base de datos: {e}")
else:
    print("No hay datos para insertar.")
