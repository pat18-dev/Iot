import json


class DbAdapter:
   def __init__(self, filename: str):
      self.filename = filename

   def save(self, json_to_db: dict):
      datos = self.get()
      datos.append(json_to_db)
      with open(self.filename, mode="w", encoding="utf-8") as f:
         json.dump(datos, f, ensure_ascii=False)
   
   def get(self):
      datos = list()
      with open(self.filename, mode="r") as f:
         datos = json.load(f)
      return datos