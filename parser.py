import pdftotext
import re
import csv

print("Introduzca el nombre del archivo")
nombre_arch = input()

if nombre_arch == "":
    nombre_arch = "target"

with open(nombre_arch + ".pdf", "rb") as f:
    pdf = "\n".join(pdftotext.PDF(f))

with open("output.txt",'w') as out:
    out.write(pdf)

pdf = pdf.split("Observacións")
pdf.pop(0)
pdf = "".join(pdf) #Borramos el encabezado
notas = re.findall("(?<=\()\d+\.\d+(?=\))", pdf)
nombres = re.findall("(?<=\,\s)((?:\w+\s)*\w+)(?=\s)", pdf)
apellidos = re.findall("(?<=\s)((?:\w+\s)*\w+)(?=\,)", pdf)
notas = [float(x) for x in notas]

#Encontramos las líneas de los no presentados, porque se escapan al regex de las notas en números

with open(nombre_arch + ".csv", mode='w', newline='') as arch_csv:
    csv_writer = csv.writer(arch_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(["Nombre","Apellidos","Nota"])
    csv_writer.writerows(zip(nombres,apellidos,notas))