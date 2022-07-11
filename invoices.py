import datetime
import check_files
import files_existence_check
import invoice_net_value
import way_out
import euro_rates


# basic variables
VAT = 0.23
BRUTTO = 1.23
NBP_RATES_FILE = "tabele_kursowe.txt"
PEKAO_RATES_FILE = "kursy_pekao.txt"
DATE_FORMAT = "%Y-%m-%d"
netto_eur_value = 0
current_date = str(datetime.datetime.now()).split()[0]
today_pekao_rate_value = 0

# Functions checking, if rate files exist     
files_existence_check.file_nbp_existence(NBP_RATES_FILE)
files_existence_check.file_pekao_existence(PEKAO_RATES_FILE)

# Functions checking, if files are up to date
check_files.file_check_nbp(NBP_RATES_FILE, DATE_FORMAT, current_date, euro_rates.today_nbp_table_no)
check_files.file_check_pekao(PEKAO_RATES_FILE, current_date, DATE_FORMAT)

# current pekao exchange rate
with open("kursy_pekao.txt", "r") as f:
    all = f.readlines()
<<<<<<< Updated upstream
    pekao_kurs = float(all[-1].split()[1].rstrip("\n"))

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

# fill the pekao file with missing exchange rates
def fill_pln_gap(start):
    current = datetime.datetime.strptime(current_date, date_format)

    start_date = datetime.datetime.strptime(start, date_format)
    end_date = current
    delta = datetime.timedelta(days=1)
    start_date += delta
    
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
              
# checking if the "tabele_kursowe.txt" file is up to date
def file_check_nbp():
    delta = datetime.timedelta(days=1)
    with open(currency_file, "r") as t:
        last = t.readlines()[-1].split()
        last_table = last[0].split("/")[0]
        date_last = last[1]
        start_date = str(datetime.datetime.strptime(date_last, date_format) + delta).split()[0]
        if today_nbp != last_table:
            fill_gap(start_date, current_date)

# checking if the "kursy_pekao.txt" file is up to date
def file_check_pekao():
    with open(pekao_file, "r") as t:
        all = t.readlines()
        if all[-1].split()[0] != current_date:
            fill_pln_gap(all[-1].split()[0])
  
# getting the right exchange rate from Pekao SA website
def pekao(date):
    with open(pekao_file, "r") as t:
        all = [k.split() for k in t.readlines()]
        for _ in all:
            if date == _[0]:
                num = all.index(_)
                kurs_pekao = float(all[num][1])
        printer_pln(kurs_pekao, date)


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
        netto_eur = input('Podaj wartość netto w EUR:\n').replace(" ", "")
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
            print("Teraz już nie jest ok")
            print(netto)
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
    nums_bools = [num for num in payment if num in signs]
    test_nums = len(nums_bools) == 10
    if not test_nums:
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
    given_date = datetime.datetime.strptime(payment, date_format)
    test_weekend = datetime.datetime.weekday(given_date) <= 4
    if not test_weekend:
        msg += "Podany dzień przypada na weekend.\n" 
    return msg

# check if date isn't in the future
def test_future(payment): 
    global msg
    given_date = datetime.datetime.strptime(payment, date_format)   
    current = datetime.datetime.strptime(current_date, date_format)
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
        if all_courses[-1][1] == current_date:
            tabela = all_courses[-2][0]
            kurs_nbp = float(all_courses[-2][2])
        else:
            tabela = all_courses[-2][0]
            kurs_nbp = float(all_courses[-2][2])
        printer_eur(tabela, kurs_nbp)

# picking the right NBP table and exchange rate for payment - from the day before
def euro(date):
    with open(currency_file, "r") as t:
        all_courses = [k.split() for k in t.readlines()]
        for _ in all_courses:
            if date == _[1]:
                num = all_courses.index(_)
                tabela = all_courses[num - 1][0]
                kurs_nbp = float(all_courses[num - 1][2])
        printer_eur(tabela, kurs_nbp)

# print the calculations in EUR
def printer_eur(tabela, kurs):
    print("\nNumer tabeli kursowej:", tabela)
    print("Kurs:", kurs)
    print(f"""
          Wartość netto EUR: {str(round(netto_eur, 2)).replace(".", ",")} €

          Wartość netto PLN: {str(round(netto_eur * kurs, 2)).replace(".", ",")} PLN

          Wartość VAT PLN: {str(round(netto_eur * kurs * vat, 2)).replace(".", ",")} PLN

          Wartość brutto EUR: {str(round(netto_eur * brutto, 2)).replace(".", ",")} €
          """)

# print the calculations in PLN
def printer_pln(kurs, date):
    print("\nKurs sprzedaży Pekao SA opublikowany {} o godzinie 7:00 wynosi {}".format(date, kurs))
    print(f"""
        Wartość netto PLN: {str(round(netto_eur * kurs, 2)).replace(".", ",")} PLN

        Wartość VAT PLN: {str(round(netto_eur * kurs * vat, 2)).replace(".", ",")} PLN

        Wartość brutto PLN: {str(round(netto_eur * kurs * brutto, 2)).replace(".", ",")} PLN
        """)

file_check_nbp()
file_check_pekao()
netto(end)
=======
    today_pekao_rate_value = float(all[-1].split()[1].rstrip("\n"))

# Main function in the program
invoice_net_value.netto(way_out.end, NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, today_pekao_rate_value)
>>>>>>> Stashed changes
