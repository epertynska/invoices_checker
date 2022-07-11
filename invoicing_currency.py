import pekao_rates, euro_rates, way_out

# pick the currency of invoicing
def main_currency(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, today_pekao_rate_value):
    global waluta
    while True:
        waluta = input("Podaj walutę, w której ma zostać wystawiona faktura (PLN/EUR)\n")
        if waluta in ("P","p", "E", "e", "PLN", "EUR"):
            if waluta in ("P", "p", "PLN"):
                pekao_rates.pln_rate_date(netto_eur_value, today_pekao_rate_value, current_date, VAT, BRUTTO)
                break
            elif waluta in ("E", "e", "EUR"):
                euro_rates.euro_date(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE)
                break
        elif waluta == "q":
            way_out.exit() 
            break
        else:
            print("Wybierz poprawną wartość.")