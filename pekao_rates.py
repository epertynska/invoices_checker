import printers
import date_input
import way_out


# getting the right exchange rate from Pekao SA rates file
def today_pekao_rate(date, PEKAO_RATES_FILE, netto_eur_value, VAT, BRUTTO):
    with open(PEKAO_RATES_FILE, "r") as t:
        all = [k.split() for k in t.readlines()]
        for _ in all:
            if date == _[0]:
                num = all.index(_)
                kurs_pekao = float(all[num][1])
        printers.printer_pln(netto_eur_value, kurs_pekao, date, VAT, BRUTTO)


# what is the date for PLN exchange rate
def pln_rate_date(netto_eur_value, today_pekao_rate_value, current_date, VAT, BRUTTO):
    while True:
        pay_date = input("Czy zastosować kurs Pekao wyemitowany dzisiaj? T/N\n")
        if pay_date in "Tt":
            printers.printer_pln(netto_eur_value, today_pekao_rate_value, current_date, VAT, BRUTTO)
            break
        elif pay_date in "Nn":
            date_input.date_input("PLN")
            break
        elif pay_date == "q":
            way_out.exit()
            break
        else:
            print("Proszę podać poprawną wartość.")

