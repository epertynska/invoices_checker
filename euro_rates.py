import json
import requests
import printers
import euro_rates
import pekao_rates
import date_input
import way_out

# current NBP table number
today_nbp_table_no = json.loads(requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/").text)['rates'][0]['no'].split("/")[0]

# taking the last NBP table for current date
def today_euro_rate(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO):
    with open(NBP_RATES_FILE, "r") as t:
        all_courses = [k.split() for k in t.readlines()]
        if all_courses[-1][1] == current_date:
            tabela = all_courses[-2][0]
            rate_date = all_courses[-2][1]
            kurs_nbp = float(all_courses[-2][2])
        else:
            tabela = all_courses[-1][0]
            rate_date = all_courses[-1][1]
            kurs_nbp = float(all_courses[-1][2])
        printers.printer_eur(netto_eur_value, tabela, kurs_nbp, VAT, BRUTTO, rate_date)

# picking the right NBP table and exchange rate for payment - from the day before
def euro_rate_for_payment(date, NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO):
    with open(NBP_RATES_FILE, "r") as t:
        all_courses = [k.split() for k in t.readlines()]
        for _ in all_courses:
            if date == _[1]:
                num = all_courses.index(_)
                tabela = all_courses[num - 1][0]
                rate_date = all_courses[num - 1][1]
                kurs_nbp = float(all_courses[num - 1][2])
        printers.printer_eur(netto_eur_value, tabela, kurs_nbp, VAT, BRUTTO, rate_date)

# pick the payment date for EUR
def euro_date(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE):
    while True:
        when = input("Czy data wpłaty jest dzisiejsza? (T/N)\n")
        if when in ("TtNn"):
            if when in "Tt":
                euro_rates.today_euro_rate(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO)
                break
            else:
                date_input.date_input("EUR", NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE)
                break
        elif when == "q":
            way_out.exit(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, pekao_rates.today_pekao_rate_value)
        else:
            print("Podaj poprawną wartość.")