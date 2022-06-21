import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# dictionary of bank holidays in 2022
bank_holidays_2022 = {"2022-01-06": "Święto Trzech Króli", "2022-04-18": "drugi dzień Wielkiej Nocy", "2022-05-03": "Święto Narodowe Konstytucji 3 Maja", "2022-06-16": "Boże Ciało", "2022-08-15": "Wniebowzięcie Najświętszej Maryi Panny, Święto Wojska Polskiego", "2022-11-01": "Wszystkich Świętych", "2022-11-11": "Narodowe Święto Niepodległości", "2022-12-26": "drugi dzień Bożego Narodzenia"}

# basic variables
vat = 0.23
brutto = 1.23
currency_file = "tabele_kursowe.txt"
date_format = "%Y-%m-%d"
ok_test = True
msg = ""
end = False
waluta = ""
netto_eur = 0
pekao_kurs = 4.8294

# current NBP table number
today_nbp = json.loads(requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/").text)['rates'][0]['no'].split("/")[0]

current_date = str(datetime.now()).split()[0]

# current pekao exchange rate
u = f"https://www.pekao.com.pl/kursy-walut/lista-walut.html?nbpDate={current_date}&pekaoDate={current_date}&debitCardDate={current_date}&reutersDate=undefined&mortgageDate={current_date}&pekaoTable=1&customerSegment=CORPO#-kursy-walut-banku-pekao-sa"
r = requests.get(u)
if r.status_code != 200:
    while True:
        pekao_kurs = input("Niestety, strona banku Pekao SA nie odpowiada. Proszę podać wartość kursu (dzielone przecinkiem):\n").replace(",", ".")
        if pekao_kurs.replace(".", "").isdigits():
            pekao_kurs = float(pekao_kurs)
            break
        else:
            print("Podaj poprawny kurs opublikowany {} o godzinie 7:00.".format(current_date))
else:
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find("table", {"class": "currencies-table"})
    currencies_list = []
    for i in table.find_all("tr", {"class": "currencies-table-item accordion-item"}):
        currencies_list.append(i)
    euro_line = currencies_list[1]
    kursy_eur = []
    for d in euro_line.find_all("td", {"class": "table-big-font"}):
        kursy_eur.append(d)
    pekao = float(str(kursy_eur[1].text).replace(",", "."))

print('W dowolnym momencie naciśnij "q" aby wyjść z programu.')

# changing the boolean variable to exit the program
def exit():
    global end
    end = True
    netto(end)

# writing all the NBP EUR currencies in the "tabele_kursowe.txt" file in given dates
def fill_gap(start, end):
    with open(currency_file, "a") as f:
        nbp_period = json.loads(requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/{}/{}/".format(start, end)).text)
        kursy = nbp_period['rates']
        upper = len(kursy)
        i = 0
        while i < upper:
            f.write(f"{kursy[i]['no']} {kursy[i]['effectiveDate']} {kursy[i]['mid']}\n")
            i += 1
          
# checking if the "tabele_kursowe.txt" file is up to date
def file_check():
    with open(currency_file, "r") as t:
        last = t.readlines()[-1].split()
        last_table = last[0].split("/")[0]
        date_last = last[1]
        if today_nbp != last_table:
            fill_gap(date_last, current_date)

# getting the right exchange rate from Pekao SA website
def pekao(date):
    url = f"https://www.pekao.com.pl/kursy-walut/lista-walut.html?nbpDate={date}&pekaoDate={date}&debitCardDate={date}&reutersDate=undefined&mortgageDate={date}&pekaoTable=1&customerSegment=CORPO#-kursy-walut-banku-pekao-sa"

    page = requests.get(url)
    if page.status_code != 200:
        while True:
            pekao = input("Niestety, strona banku Pekao SA nie odpowiada. Proszę podać wartość kursu (dzielone przecinkiem):\n").replace(",", ".")
            if pekao.replace(".", "").isdigits():
                pekao = float(pekao)
                break
            elif pekao == "q":
                exit()
                break
            else:
                print("Podaj poprawny kurs opublikowany {} o godzinie 7:00.".format(date))
    else:
        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.find("table", {"class": "currencies-table"})

        currencies = []

        for i in table.find_all("tr", {"class": "currencies-table-item accordion-item"}):
            currencies.append(i)
        euro_row = currencies[1]
        kursy = []
        for d in euro_row.find_all("td", {"class": "table-big-font"}):
            kursy.append(d)
        pekao = float(str(kursy[1].text).replace(",", "."))
    printer_pln(pekao, date)

# what is the date for PLN exchange rate
def pln():
    pay_date = input("Czy zastosować kurs Pekao wyemitowany dzisiaj? (T/N)\n")
    if pay_date in ("Tt"):
        printer_pln(pekao_kurs, current_date)
    elif pay_date in ("Nn"):
        date_input("PLN")
    elif pay_date == "q":
        exit()

# taking net value of invoice in EUR currency
def netto(finish):
    global netto_eur, end
    while True:
        if end is True:
            break
        netto_eur = input('Podaj wartość netto w EUR:\n')
        if netto_eur == "q":
            break
        try:
            positive = float(netto_eur.replace(",", ".")) > 0
            if "," in netto_eur and positive:
                netto_eur = float(netto_eur.replace(",", "."))
            elif positive:
                netto_eur = float(netto_eur)
            else:
                raise Exception()
            main_currency()
        except ValueError:
            print("Proszę podać poprawną wartość.")
        except Exception:
            print("Wartość musi być większa od zera.")

# checking if date is given in the right format and length
def test_format(payment):
    global msg, ok_test
    check = payment.split("-")
    test_check = len(check) == 3
    if not test_check or not check:
        msg += "Powinna się składać z 3 liczb oddzielonych myślnikami.\n"
        ok_test = False
    return msg

# checking if given date contains only numbers and "-"
def test_digits(payment):
    global msg, ok_test
    signs = ("1234567890-")
    nums_bools = [num.isdigit() for num in payment.replace("-", "")]
    test_nums = all(nums_bools)
    if test_nums:
        right_symbols = [s in signs for s in payment]
        test_right = all(right_symbols)
    else:
        right_symbols = False
        test_right = False
    if not test_right or not test_nums:
        msg += "Data powinna się składać z cyfr i myślników.\n"
        ok_test = False
    return msg

# testing if given data is in YYYY-MM-DD format
def test_length(payment):
    global msg, ok_test
    check = payment.split("-")
    if len("".join(check)) == 8:
        test_length = len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2 
    else:
        test_length = False
    if not test_length or not check:
        msg += "Data powinna być wpisana w systemie 4-2-2.\n"
        ok_test = False
    return msg

# test of given data existence
def test_real(payment):
    global msg, ok_test
    check = payment.split("-")
    if len("".join(check)) == 8:
        test_date = int(check[0]) <= int(str(current_date).split("-")[0]) and (int(check[1]) > 0 and int(check[1]) <= 12) and (int(check[2]) > 0 and int(check[2]) <= 31)
    else:
        test_date = False
    if not test_date or not check:
        msg += "Taka data nie istnieje.\n"
        ok_test = False
    return msg

# weekend days check
def test_weekend(payment):
    global msg
    given_date = datetime.strptime(payment, date_format)
    test_weekend = datetime.weekday(given_date) <= 4
    if not test_weekend:
        msg += "Podany dzień przypada na weekend.\n" 
    return msg

# check if date isn't in the future
def test_future(payment): 
    global msg
    given_date = datetime.strptime(payment, date_format)   
    current = datetime.strptime(current_date, date_format)
    test_f = given_date <= current
    if not test_f:
        msg += "Podany dzień jeszcze nie nastąpił.\n"
    return msg

# bank holidays check
def test_holidays(payment):
    global msg
    test_bank_holiday = payment not in bank_holidays_2022
    if not test_bank_holiday:
        msg += "\nTen dzień to {}.".format(bank_holidays_2022[payment])
    return msg

# taking date of payment
def date_input(currency):
    global msg, ok_test
    while True:
        payment = input("Podaj datę wpływu na konto: (RRRR-MM-DD)\n")
        msg_1 = "Data jest niepoprawna.\n"
        
        test_format(payment)
        test_digits(payment)
        test_length(payment)
        test_real(payment)
        if ok_test is True:
            test_weekend(payment)
            test_future(payment)
            test_holidays(payment)

      
        if msg == "":
            if currency == "EUR":
                euro(payment)
                break
            else:
                pekao(payment)
                break
        elif payment == "q":
            exit()
            break
        else:
            print(msg_1 + msg)
            msg = ""
            ok_test = True

# pick the currency of invoicing
def main_currency():
    global waluta
    while True:
        waluta = input("Podaj walutę, w której ma zostać wystawiona faktura (PLN/EUR)\n")
        if waluta in ("P","p", "E", "e", "PLN", "EUR"):
            if waluta in ("P", "p", "PLN"):
                pln()
                break
            elif waluta in ("E", "e", "EUR"):
                euro_date()
                break
        elif waluta == "q":
            exit() 
            break
        else:
            print("Wybierz poprawną wartość.")

# pick the payment date for WUR
def euro_date():
    while True:
        when = input("Czy data wpłaty jest dzisiejsza? (T/N)\n")
        if when in ("TtNn"):
            if when in "Tt":
                euro_today()
                break
            else:
                date_input("EUR")
                break
        else:
            print("Podaj poprawną wartość.")

# taking the last NBP table for current date
def euro_today():
    with open(currency_file, "r") as t:
        all_courses = [k.split() for k in t.readlines()]
        tabela = all_courses[-1][0]
        kurs_nbp = float(all_courses[-1][2])
        print("Numer tabeli kursowej:", tabela)
        print("Kurs:", kurs_nbp)
        printer_eur(kurs_nbp)

# picking the right NBP table and exchange rate for payment - from the day before
def euro(date):
    with open(currency_file, "r") as t:
        all_courses = [k.split() for k in t.readlines()]
        for _ in all_courses:
            if date == _[1]:
                num = all_courses.index(_)
                tabela = all_courses[num - 1][0]
                kurs_nbp = float(all_courses[num - 1][2])
        print("Numer tabeli kursowej:", tabela)
        print("Kurs:", kurs_nbp)
        printer_eur(kurs_nbp)

# print the calculations in EUR
def printer_eur(kurs):
    print(f"""
          Wartość netto EUR: {str(round(netto_eur, 2)).replace(".", ",")} €

          Wartość netto PLN: {str(round(netto_eur * kurs, 2)).replace(".", ",")} PLN

          Wartość VAT PLN: {str(round(netto_eur * kurs * vat, 2)).replace(".", ",")} PLN

          Wartość brutto EUR: {str(round(netto_eur * brutto, 2)).replace(".", ",")} €
          """)

# print the calculations in PLN
def printer_pln(kurs, date):
    print("Kurs sprzedaży opublikowany {} o godzinie 7:00 wynosi {}".format(date, kurs))
    print(f"""
        Wartość netto PLN: {str(round(netto_eur * kurs, 2)).replace(".", ",")} PLN

        Wartość VAT PLN: {str(round(netto_eur * kurs * vat, 2)).replace(".", ",")} PLN

        Wartość brutto PLN: {str(round(netto_eur * kurs * brutto, 2)).replace(".", ",")} PLN
        """)

file_check()

netto(end)