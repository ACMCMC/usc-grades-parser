# usc-grades-parser
## [EN]
## Python 3 script to automatically obtain statistical measures from grades PDFs from the USC
This script starts taking a set of PDF grades documents from the University of Santiago de Compostela (provisional or definitive grades), whose names are specified at runtime, and parses the documents to get statistical measures from them (mean, median). Additionally, it saves the grades on CSV files (named after the subjects' codes), for them to be used with other programs. It also creates a final report of results.

---

## [ES]
## Script de Python 3 para obtener automáticamente las estadísticas de PDFs de cualificaciones de la USC
Este repositorio incluye un script que, partiendo de un documento PDF de cualificaciones (provisionales o definitivas) de la Universidad de Santiago de Compostela, cuyo nombre se indica en tiempo de ejecución, recupera automáticamente los datos del mismo y ofrece estadísticas sobre ellos. Igualmente, guarda los datos en un CSV (con un nombre que se genera a partir del código de la asignatura), separados por ```';'```, para su posible uso con otros programas. También crea un informe final de resultados.

---

**Dependencies** (*Dependencias*):

- Popper
- pdftotext
