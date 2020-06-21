import pdftotext
import re
import csv
import sys
import os
from statistics import mean, median

def parse_arch(path_archivo):
    with open(path_archivo, "rb") as f:
        pdf = "\n".join(pdftotext.PDF(f))

    # with open("output.txt",'w') as out:
    #    out.write(pdf)

    tipo_listaxe = re.search("(?<=Listaxe\s)(provisoria|definitiva)", pdf).group(0) #Extraemos el tipo de lista que es, para crear el nombre del CSV
    nombre_materia = re.search("(?<=Materia:)\s+(?:\w+\s)*\w+", pdf).group(0).lstrip() #Extraemos el nombre de la materia
    codigo_materia = re.search("\w+", nombre_materia).group(0)
    nombre_materia = nombre_materia.replace(codigo_materia, '').lstrip()

    pdf = pdf.split("Observacións") #Borramos el encabezado
    pdf.pop(0)
    pdf = "".join(pdf)  

    #Hacemos un regex para obtener los datos
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

    with open(os.path.dirname(path_archivo) + "/" + tipo_listaxe.upper() + "_" + codigo_materia + ".csv", mode='w', newline='') as arch_csv:
        csv_writer = csv.writer(arch_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(["Apellidos", "Nombre", "Nota"])
        csv_writer.writerows(zip(apellidos, nombres, notas))

    # Calculamos parámetros estadísticos
    nombres_parametros = ["media", "mediana"]
    valores_parametros = [mean(notas), median(notas)]
    parametros = zip(nombres_parametros, valores_parametros)
    print("\n" + nombre_materia + " [" + codigo_materia + "]:\n" + "\n".join(list(map(lambda x: ": ".join((x[0], str(x[1]))), parametros))))

#COMPROBAMOS SI EXISTE UN SUBDIRECTORIO
lista_directorio = next(os.walk(os.getcwd()))[1] #Listamos los subdirectorios inmediatos
lista_directorio = list(filter(lambda x: x[0] != '.', lista_directorio)) #Eliminamos los directorios que empiezan por '.'; p. ej, ".git"
lista_paths = [] #Aún no sabemos el/los nombre(s) de nuestro(s) archivo(s)

if len(sys.argv) == 2:
    lista_paths = [sys.argv[1]]
elif len(lista_directorio) > 0:
    print("Se han encontrado los siguientes subdirectorios:")
    print("\t" + "\n\t".join(lista_directorio))
    print("Desea utilizar uno de ellos como carpeta de filtrado? (S/N)")
    if input() == "S":
        while lista_paths == []:
            #Seleccionar el subdirectorio
            print("Escriba el nombre del subdirectorio:")
            #Obtenemos el nombre del subdirectorio
            nombre_subdir = None
            while nombre_subdir not in lista_directorio:
                nombre_subdir = input()

            lista_paths = list(map(lambda x: nombre_subdir+'/'+x, filter(lambda x: ".pdf" in x, next(os.walk(os.getcwd()+"/"+nombre_subdir))[2])))
            
            if lista_paths == []:
                print("No se han encontrado archivos PDF. Por favor, seleccione otro subdirectorio.")

while lista_paths == [] or lista_paths == [""]:
    print("Introduzca el nombre del archivo:")
    lista_paths = [input()]

print("Se va a analizar " + lista_paths[0] if len(lista_paths) == 1 else "Se van a analizar:\n\t" + "\n\t".join(lista_paths))

resultados = list(map(parse_arch, lista_paths))