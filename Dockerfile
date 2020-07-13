FROM python:3
ADD parse.py /
RUN pip install popper
RUN pip install pdftotext
CMD ["python", "parse.py"]
