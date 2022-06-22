import json
import requests
import datetime
from bs4 import BeautifulSoup

currency_file = "tabele_kursowe.txt"

# Pekao PLN rates
date_format = "%Y-%m-%d"
current_date = str(datetime.datetime.now()).split()[0]
current = datetime.datetime.strptime(current_date, date_format)

start_date = datetime.datetime.strptime("2022-01-01", date_format)
end_date = current
delta = datetime.timedelta(days=1)

while start_date <= end_date:
    day = str(start_date).split()[0]
    start_date += delta
    with open("kursy_pekao.txt", "a") as p:
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

# NBP tables file creation
with open(currency_file, "a") as f:
    start = "2022-01-01"
    end = current_date
    nbp_period = json.loads(requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/{}/{}/".format(start, end)).text)
    kursy = nbp_period['rates']
    upper = len(kursy)
    i = 0
    while i < upper:
        f.write(f"{kursy[i]['no']} {kursy[i]['effectiveDate']} {kursy[i]['mid']}\n")
        i += 1