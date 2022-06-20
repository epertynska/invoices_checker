import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup


# dictionary of bank holidays in 2022
bank_holidays_2022 = {"2022-01-06": "Święto Trzech Króli", "2022-04-18": "drugi dzień Wielkiej Nocy", "2022-05-03": "Święto Narodowe Konstytucji 3 Maja", "2022-06-16": "Boże Ciało", "2022-08-15": "Wniebowzięcie Najświętszej Maryi Panny, Święto Wojska Polskiego", "2022-11-01": "Wszystkich Świętych", "2022-11-11": "Narodowe Święto Niepodległości", "2022-12-26": "drugi dzień Bożego Narodzenia"}

netto_eur = 0
vat = 0.23
brutto = 1.23
currency = ""
currency_file = "tabele_kursowe.txt"

# current NBP table number
today_nbp = json.loads(requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/").text)['rates'][0]['no'].split("/")[0]

current_date = str(datetime.now()).split()[0]


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
          

def file_check():
    with open(currency_file, "r") as t:
        last = t.readlines()[-1].split()
        last_table = last[0].split("/")[0]
        date_last = last[1]
        if today_nbp != last_table:
            fill_gap(date_last, current_date)


def pln(date):
    url = f"https://www.pekao.com.pl/kursy-walut/lista-walut.html?nbpDate={date}&pekaoDate={date}&debitCardDate={date}&reutersDate=undefined&mortgageDate={date}&pekaoTable=1&customerSegment=CORPO#-kursy-walut-banku-pekao-sa"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    if page.status_code != 200:
        pekao = input("Niestety, strona banku Pekao SA nie odpowiada. Proszę podać wartość kursu:\n")
    else:
        pekao = 0
        print(soup.find("tbody"))


# taking net value of invoice in EUR currency
def netto():
    global netto_eur
    while True:
        netto_eur = input("Podaj wartość netto w EUR:\n")
        try:
            if "," in netto_eur:
                netto_eur = float(netto_eur.replace(",", "."))
            else:
                netto_eur = float(netto_eur)
            waluta()
        except Exception:
            print("Proszę podać poprawną wartość.")

 
# taking date of payment
def date_input(currency):
    global current_date
    while True:
        payment = input("Podaj datę wpływu na konto: (RRRR-MM-DD)\n")
        signs = [str(n) for n in range(10)]
        signs.append("-")
        signs = "".join(signs)
        msg = "Data jest niepoprawna."
      
        try:
            # test liczb i myślników
            right_symbols = [s in signs for s in payment]
            # print("lista znaków w poprawnych:", right_symbols)
            test_right = all(right_symbols)
            # print("Test czy lista boolean poprawna:", test_right)
            check = payment.split("-")
            # print("test check:", check)
            test_check = len(check) == 3
            # print("Test check długość:", test_check)
            if not test_check:
                msg += "\nPowinna się składać z 3 liczb oddzielonych myślnikami.\n"
                raise Exception(msg)
    
              
            # test liczb
            nums_bools = [num.isdigit() for num in check]
            # print("Lista numerów:", nums_bools)
            test_nums = all(nums_bools)
            # print("Test wszystkich nums bools:", test_nums)
            if not test_right or not test_nums:
                msg = "\nData powinna się składać z cyfr i myślników.\n"
                raise Exception(msg)
            
    
            #Test długości poszczególnych elementów
            test_length = len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2
            if not test_length or not right_symbols:
                msg += "\nData powinna być wpisana w systemie 4-2-2.\n"
                raise Exception(msg)
            # print("długość liczb:", test_length)
    
            # Test poprawności dat
            test_date = int(check[0]) <= int(str(current_date).split("-")[0]) and (int(check[1]) > 0 and int(check[1]) <= 12) and (int(check[2]) > 0 and int(check[2]) <= 31)
            if not test_date:
                msg += "\nTaki data jest nierealna.\n"
                raise Exception(msg)
            # print("test date", test_date)
    
            # weekend days check
            given_date = datetime.strptime(payment, "%Y-%m-%d")
            test_weekend = datetime.weekday(given_date) <= 4
            if not test_weekend:
                msg += "\nPodany dzień przypada na weekend.\n"  
                raise Exception(msg)

              
            # future date check
            current = datetime.strptime(current_date, "%Y-%m-%d")
            test_future = given_date <= current
            if not test_future:
                msg += "\nPodany dzień jeszcze nie nastąpił."
                raise Exception(msg)

            # bank holidays check
            test_bank_holiday = payment not in bank_holidays_2022
            if not test_bank_holiday:
                msg += "\nTen dzień to {}.".format(bank_holidays_2022[payment])
                raise Exception(msg)
            # print("święto", test_bank_holiday)

            if test_check and test_date and test_length and test_nums and test_right and test_weekend and test_bank_holiday:
                if currency == "EUR":
                    euro(payment)
                    break
                else:
                    pln(payment)
                    break
        except Exception:
            print(msg)




def waluta():
    global currency
    while True:
        waluta = input("Podaj walutę, w której ma zostać wystawiona faktura (PLN/EUR)\n")
        if waluta in ("P","p", "E", "e", "PLN", "EUR"):
            if waluta in ("P", "p", "PLN"):
                currency = "PLN"
                when = input("Czy data emisji kursu jest dzisiejsza? (T/N)\n")
                if when in ("TtNn"):
                    if when in "Tt":
                        pln(current_date)
                        break
                    else:
                        date_input(currency)
                        break
            elif waluta in ("E", "e", "EUR"):
                currency = "EUR"
                when = input("Czy data wpłaty jest dzisiejsza? (T/N)\n")
                if when in ("TtNn"):
                    if when in "Tt":
                        euro(current_date)
                        break
                    else:
                        date_input(currency)
                        break
        else:
            print("Wybierz poprawną wartość.")


def euro(date):
    with open("tabele_kursowe.txt", "r") as t:
        all_courses = [k.split() for k in t.readlines()]
        for _ in all_courses:
            if date == _[1]:
                num = all_courses.index(_)
                tabela = all_courses[num - 1][0]
                kurs_NBP = float(all_courses[num - 1][2])
            else:
                tabela = all_courses[-1][0]
                kurs_NBP = float(all_courses[-1][2])
        print("Numer tabeli kursowej:", tabela)
        print("Kurs:", kurs_NBP)
        printer_eur(kurs_NBP)


def printer_eur(kurs_NBP):
    global netto_eur, vat, brutto
    print(f"""
          Wartość netto EUR: {str(round(netto_eur, 2)).replace(".", ",")} €

          Wartość netto PLN: {str(round(netto_eur * kurs_NBP, 2)).replace(".", ",")} PLN

          Wartość VAT PLN: {str(round(netto_eur * kurs_NBP * vat, 2)).replace(".", ",")} PLN

          Wartość brutto EUR: {str(round(netto_eur * brutto, 2)).replace(".", ",")} €
          """)


netto()