import json
import datetime
import requests
from bs4 import BeautifulSoup

# writing all the NBP EUR currencies in the "tabele_kursowe.txt" file in given dates
def fill_eur_gap(start, end, NBP_RATES_FILE):
    print("Aktualizuję plik z tabelami NBP, proszę o chwilę cierpliwości.")
    with open(NBP_RATES_FILE, "a") as f:
        nbp_period = json.loads(requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/{}/{}/".format(start, end)).text)
        kursy = nbp_period['rates']
        upper = len(kursy)
        i = 0
        while i < upper:
            f.write(f"{kursy[i]['no']} {kursy[i]['effectiveDate']} {kursy[i]['mid']}\n")
            i += 1
    print("Plik z tabelami NBP został pomyślnie zaktualizowany.")
    return

# fill the pekao file with missing exchange rates
def fill_pln_gap(start, current_date, DATE_FORMAT, PEKAO_RATES_FILE):
    current = datetime.datetime.strptime(current_date, DATE_FORMAT)
  
    start_date = datetime.datetime.strptime(start, DATE_FORMAT)
    end_date = current
    delta = datetime.timedelta(days=1)
    start_date += delta
    print("Aktualizuję plik z kursami Pekao, proszę o chwilę cierpliwości.")
    while start_date <= end_date:
        day = str(start_date).split()[0]
        start_date += delta
        with open(PEKAO_RATES_FILE, "a") as p:
            url = f"https://www.pekao.com.pl/kursy-walut/lista-walut.html?nbpDate={day}&pekaoDate={day}&debitCardDate={day}&reutersDate=undefined&mortgageDate={day}&pekaoTable=1&customerSegment=CORPO#-kursy-walut-banku-pekao-sa"
            page = requests.get(url)
            if page.status_code != 200:
                continue
            else:
                soup = BeautifulSoup(page.text, 'lxml')
                tbl = soup.find("table", {"class": "currencies-table"})
        
                currencies = []
                try:
                    info = str(soup.find("h2", {"class": "cl-flag table-big-font text-center"}).text).strip()
                    if info == "Brak kursu z danego dnia, proszę wybrać inną datę.":
                        continue
                except AttributeError:
                    for i in tbl.find_all("tr", {"class": "currencies-table-item accordion-item"}):
                        currencies.append(i)
                    euro_row = currencies[1]
                    kursy = []
                    for d in euro_row.find_all("td", {"class": "table-big-font"}):
                        kursy.append(d)
                    pekao = float(str(kursy[1].text).replace(",", "."))
                    p.write(day + " " + str(pekao) + "\n")
    print("Plik z kursami Pekao został pomyślnie zaktualizowany.")
    return