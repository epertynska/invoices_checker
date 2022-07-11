import os
import files_creation

#check if rates files exist
def file_nbp_existence(NBP_RATES_FILE):
  if not os.access(NBP_RATES_FILE, os.F_OK):
      print("Tworzę plik zawierający tabele kursów NBP. Chwilę mi to zajmie, proszę o cierpliwość...")
      files_creation.nbp_rates_file_create()
  else:
      print("Plik z tabelami NBP istnieje, nie trzeba go tworzyć.")

def file_pekao_existence(PEKAO_RATES_FILE):
  if not os.access(PEKAO_RATES_FILE, os.F_OK):
      print("Tworzę plik zawierający kursy sprzedaży Pekao. Chwilę mi to zajmie, proszę o cierpliwość...")
      files_creation.pekao_rates_file_create()
  else:
      print("Plik z kursami Pekao istnieje, nie trzeba go tworzyć.")