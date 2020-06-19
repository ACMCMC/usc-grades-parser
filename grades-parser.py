import pdftotext

print("Introduzca el nombre del archivo")
nombre_arch = input()

with open(nombre_arch + ".pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

with open("output.txt",'w') as out:
    out.write("\n".join(pdf))

#Añadir método de filtrado