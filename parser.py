import pdftotext
import re
import csv
import statistics

print("Introduzca el nombre del archivo:")
nombre_arch = input()

if nombre_arch == "":
    nombre_arch = "target"
    print("Tomando " + nombre_arch + ".pdf como nombre por defecto.")

with open(nombre_arch if ".pdf" in nombre_arch else nombre_arch + ".pdf", "rb") as f:
    pdf = "\n".join(pdftotext.PDF(f))

# with open("output.txt",'w') as out:
#    out.write(pdf)

pdf = pdf.split("Observacións")
pdf.pop(0)
pdf = "".join(pdf)  # Borramos el encabezado
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

with open(nombre_arch.replace(".pdf", ".csv") if ".pdf" in nombre_arch else nombre_arch + ".csv", mode='w', newline='') as arch_csv:
    csv_writer = csv.writer(arch_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(["Apellidos", "Nombre", "Nota"])
    csv_writer.writerows(zip(apellidos, nombres, notas))

# Calculamos parámetros estadísticos
nombres_parametros = ["media", "mediana"]
valores_parametros = [statistics.mean(notas), statistics.median(notas)]
parametros = zip(nombres_parametros, valores_parametros)
print("\nPARAMETROS\n" + "\n".join(list(map(lambda x: ": ".join((x[0], str(x[1]))), parametros))))
