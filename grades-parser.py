import pdftotext

with open("Target.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

with open("output.txt",'w') as out:
    out.write("\n\n".join(pdf))