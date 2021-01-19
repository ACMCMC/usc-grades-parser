import pdftotext
import re
import csv
import sys
import os
from statistics import mean, median

# coding=utf-8

#TODO: Anadir soporte para formatos de notas no estandares

def parse_arch(path_archivo):
    with open(path_archivo, "rb") as f:
        pdf = "\n".join(pdftotext.PDF(f))

    # with open("output.txt",'w') as out:
    #    out.write(pdf)

    tipo_listaxe = re.search("(?<=Listaxe\s)(provisoria|definitiva)", pdf).group(
        0)  # Extraemos el tipo de lista que es, para crear el nombre del CSV
    # Extraemos el nombre de la materia
    nombre_materia = re.search(
        "(?<=Materia:)\s+(?:\w+\s)*\w+", pdf).group(0).lstrip()
    codigo_materia = re.search("\w+", nombre_materia).group(0)
    nombre_materia = nombre_materia.replace(codigo_materia, '').lstrip()

    pdf = pdf.split("Observacións")  # Borramos el encabezado
    pdf.pop(0)
    pdf = "".join(pdf)

    # Hacemos un regex para obtener los datos
    notas = re.findall("(?<=\()\d+\.\d+(?=\))", pdf)
    nombres = re.findall("(?<=\,\s)((?:\w+\s)*\w+)(?=\s)", pdf)
    apellidos = re.findall("(?<=\s)((?:\d+\s)*\w+)(?=\,)", pdf)
    notas = [float(x) for x in notas]

    # Encontramos las líneas de los no presentados, porque se escapan al regex de las notas en números
    no_presentados = list(
        map(lambda x: int(x)-1, re.findall("\d+(?=\s.+Non\sPresentado)", pdf)))
    #list(map(lambda x: nombres.pop(int(x)-1), no_presentados))
    nombres = list(map(lambda x: x[1], filter(
        lambda tupla: True if tupla[0] not in no_presentados else False, enumerate(nombres))))
    apellidos = list(map(lambda x: x[1], filter(
        lambda tupla: True if tupla[0] not in no_presentados else False, enumerate(apellidos))))
    #[nombres[index_nombre] for index_nombre in range(nombres) if index_nombre not in no_presentados]

    with open(os.path.dirname(os.path.abspath(path_archivo)) + "/" + tipo_listaxe.upper() + "_" + codigo_materia + ".csv", mode='w', newline='') as arch_csv:
        csv_writer = csv.writer(arch_csv, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(["Apellidos", "Nombre", "Nota"])
        csv_writer.writerows(zip(apellidos, nombres, notas))

    # Calculamos parámetros estadísticos
    parametros = {
        "total de presentados": len(notas),
        "media": mean(notas),
        "mediana": median(notas)}
    with open("INFORME.txt", 'a') as archivo_informe:
        archivo_informe.write(
            nombre_materia + " [" + codigo_materia + "] (" + tipo_listaxe.upper() + "):\n\t")
        archivo_informe.writelines("\n\t".join(
            list(map(lambda item: ": ".join((item[0], str(item[1]))), parametros.items()))))
        archivo_informe.write("\n\n")


# COMPROBAMOS SI EXISTE UN SUBDIRECTORIO
# Listamos los subdirectorios inmediatos
lista_directorio = next(os.walk(os.getcwd()))[1]
# Eliminamos los directorios que empiezan por '.'; p. ej, ".git"
lista_directorio = list(filter(lambda x: x[0] != '.', lista_directorio))
lista_paths = []  # Aún no sabemos el/los nombre(s) de nuestro(s) archivo(s)

if len(sys.argv) == 2:
    lista_paths = [sys.argv[1]]
elif len(lista_directorio) > 0:
    print("Se han encontrado los siguientes subdirectorios:")
    print("\t" + "\n\t".join(lista_directorio))
    print("Desea utilizar uno de ellos como carpeta de filtrado? (S/N)")
    if input() == "S":
        while lista_paths == []:
            # Seleccionar el subdirectorio
            print("Escriba el nombre del subdirectorio:")
            # Obtenemos el nombre del subdirectorio
            nombre_subdir = None
            while nombre_subdir not in lista_directorio:
                nombre_subdir = input()

            lista_paths = list(map(lambda x: nombre_subdir+'/'+x, filter(
                lambda x: ".pdf" in x, next(os.walk(os.getcwd()+"/"+nombre_subdir))[2])))

            if lista_paths == []:
                print(
                    "No se han encontrado archivos PDF. Por favor, seleccione otro subdirectorio.")

while lista_paths == [] or lista_paths == [""]:
    print("Introduzca el nombre del archivo:")
    lista_paths = [input()]

print("Se va a analizar " + lista_paths[0] if len(lista_paths)
      == 1 else "Se van a analizar:\n\t" + "\n\t".join(lista_paths))

open('INFORME.txt', 'w').close()

resultados = list(map(parse_arch, lista_paths))
