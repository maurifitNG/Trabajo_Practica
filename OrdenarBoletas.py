import os
import shutil
import datetime

# Directorios
base_directory = r"C:\Users\mauri\OneDrive\Escritorio\Portafolio\Boletas-servidores"
resultados_directory = r"C:\Users\mauri\OneDrive\Escritorio\Portafolio\Boletas-main"

# Crear carpeta de resultados si no existe
os.makedirs(resultados_directory, exist_ok=True)
print(f"Carpeta de resultados creada: {resultados_directory}")

# Función para procesar archivos .ted y .txt
def process_file(file_path):
    try:
        # Obtener la fecha de modificación del archivo
        mod_time = os.path.getmtime(file_path)
        mod_date = datetime.datetime.fromtimestamp(mod_time)
        print(f"Fecha de modificación para {file_path}: {mod_date.strftime('%Y-%m-%d')}")

        # Crear carpetas de Año y Mes
        year_folder = os.path.join(resultados_directory, str(mod_date.year))
        month_folder = os.path.join(year_folder, mod_date.strftime('%m-%B'))
        os.makedirs(month_folder, exist_ok=True)

        # Extraer los primeros 10 caracteres del nombre del archivo (sin la extensión)
        base_name = os.path.splitext(os.path.basename(file_path))[0][:10]

        # Crear subcarpeta con los primeros 10 caracteres del nombre del archivo
        name_folder = os.path.join(month_folder, base_name)
        os.makedirs(name_folder, exist_ok=True)

        # Copiar el archivo a la subcarpeta con el nombre
        dest_path = os.path.join(name_folder, os.path.basename(file_path))
        
        # Verificar si ya existe un archivo con el mismo nombre y agregar un sufijo si es necesario
        if os.path.exists(dest_path):
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(name_folder, f"{base_name}_{counter}{os.path.splitext(file_path)[1]}")
                counter += 1

        shutil.copy2(file_path, dest_path)  # Cambiar a shutil.copy2
        print(f"Archivo {file_path} copiado a {dest_path}")

    except Exception as e:
        print(f"Error al procesar '{file_path}': {str(e)}")

# Procesar las subcarpetas en el directorio base
for root, dirs, files in os.walk(base_directory):
    for file in files:
        if file.endswith(".ted") or file.endswith(".txt"):
            file_path = os.path.join(root, file)
            print(f"Procesando archivo: {file_path}")
            process_file(file_path)
