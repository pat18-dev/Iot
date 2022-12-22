import csv


class DbAdapter:
   def __init__(self, filename: str):
      self.filename = filename

   def save(self, datos: list):
      with open(self.filename, mode="w", encoding="utf-8") as f:
         AdapterWriter = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
         AdapterWriter.writerow(datos)
   
   def get(self):
      datos = list()
      with open(self.filename, mode="r", encoding="utf-8") as csv_file:
         csv_reader = csv.reader(csv_file, delimiter=',')
         for item in csv_reader:
            datos.append(item)
      return datos