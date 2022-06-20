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

# current NBP table number
today_nbp = json.loads(requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/").text)['rates'][0]['no'].split("/")[0]

current_date = str(datetime.now()).split()[0]

# changing the boolean variable to exit the program
def exit():
    global end
    end = True
    return end

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
        pekao = input("Niestety, strona banku Pekao SA nie odpowiada. Proszę podać wartość kursu (dzielone przecinkiem):\n").replace(",", ".")
        if pekao.replace(".", "").isdigits():
            pekao = float(pekao)
        elif pekao == "q":
            exit()
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
        pekao(current_date)
    elif pay_date in ("Nn"):
        date_input("PLN")
    elif pay_date == "q":
        exit()

# taking net value of invoice in EUR currency
def netto():
    global netto_eur
    while True:
        netto_eur = input('Podaj wartość netto w EUR lub naciśnij "q" aby wyjść:\n')
        if netto_eur == "q":
            exit()
            break
        else:
            try:
                netto_eur = float(netto_eur.replace(",", "."))
                return netto_eur
            except ValueError:
                print("Proszę podać poprawną wartość.")

# checking if date is given in the right format and length
def test_format(payment):
    global ok_test, msg
    check = payment.split("-")
    test_check = len(check) == 3
    if not test_check:
        msg += "\nPowinna się składać z 3 liczb oddzielonych myślnikami.\n"
        ok_test = False
    return msg, ok_test

# checking if given date contains only numbers and "-"
def test_digits(payment):
    global ok_test, msg
    signs = ("1234567890-")
    nums_bools = [num.isdigit() for num in payment.replace("-", "")]
    test_nums = all(nums_bools)
    right_symbols = [s in signs for s in payment]
    test_right = all(right_symbols)
    if not test_right or not test_nums:
        msg += "\nData powinna się składać z cyfr i myślników.\n"
        ok_test = False
    return msg, ok_test

# testing if given data is in YYYY-MM-DD format
def test_length(payment):
    global ok_test, msg
    check = payment.split("-")
    test_length = len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2
    if not test_length:
        msg += "\nData powinna być wpisana w systemie 4-2-2.\n"
        ok_test = False
    return msg, ok_test

# test of given data existence
def test_real(payment):
    global ok_test, msg
    check = payment.split("-")
    test_date = int(check[0]) <= int(str(current_date).split("-")[0]) and (int(check[1]) > 0 and int(check[1]) <= 12) and (int(check[2]) > 0 and int(check[2]) <= 31)
    if not test_date:
        msg += "\nTaka data jest nie istnieje.\n"
        ok_test = False
    return msg, ok_test

# weekend days check
def test_weekend(payment):
    global ok_test, msg
    given_date = datetime.strptime(payment, date_format)
    test_weekend = datetime.weekday(given_date) <= 4
    if not test_weekend:
        msg += "\nPodany dzień przypada na weekend.\n" 
        ok_test = False
    return msg, ok_test

# check if date isn't in the future
def test_future(payment): 
    global ok_test, msg
    given_date = datetime.strptime(payment, date_format)   
    current = datetime.strptime(current_date, date_format)
    test_future = given_date <= current
    if not test_future:
        msg += "\nPodany dzień jeszcze nie nastąpił."
        ok_test = False
    return msg, ok_test

# bank holidays check
def test_holidays(payment):
    global ok_test, msg
    test_bank_holiday = payment not in bank_holidays_2022
    if not test_bank_holiday:
        msg += "\nTen dzień to {}.".format(bank_holidays_2022[payment])
        ok_test = False
    return msg, ok_test

# taking date of payment
def date_input(currency):
    global ok_test
    while True:
        payment = input("Podaj datę wpływu na konto: (RRRR-MM-DD)\n")
        msg_1 = "Data jest niepoprawna.\n"
      
        test_format(payment)
        test_digits(payment)
        test_length(payment)
        test_real(payment)
        test_weekend(payment)
        test_future(payment)
        test_holidays(payment)

        if msg == "" and ok_test:
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
            print(msg_1, msg)

# pink the currency of invoice
def main_currency():
    global waluta
    while True:
        waluta = input("Podaj walutę, w której ma zostać wystawiona faktura (PLN/EUR)\n")
        if waluta in ("P","p", "E", "e", "PLN", "EUR"):
            return waluta
        elif waluta == "q":
            exit()    
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

while not end:
    netto()
    main_currency()
    if waluta in ("P", "p", "PLN"):
        pln()
    elif waluta in ("E", "e", "EUR"):
        euro_date() 