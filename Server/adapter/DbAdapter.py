import csv


class DbAdapter:
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, datos: list):
        with open(self.filename, mode="a", newline='', encoding="utf-8") as csv_file:
            AdapterWriter = csv.writer(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            AdapterWriter.writerow(datos)
            csv_file.close()

    def get(self):
        datos = list()
        with open(self.filename, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for item in csv_reader:
                if item:
                    datos.append(item)
        return datos
