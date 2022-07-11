import invoicing_currency, way_out

# taking net value of invoice in EUR currency
def netto(finish, NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, today_pekao_rate_value):
    while True:
        if way_out.end is True:
            break
        print('W dowolnym momencie naciśnij "q" aby wyjść z programu.')
        netto_eur = input('Podaj wartość netto w EUR:\n').replace(" ", "")
        if netto_eur == "q":
            break
        try:
            positive = float(netto_eur.replace(",", ".")) > 0
            if "," in netto_eur and positive:
                netto_eur_value = float(netto_eur.replace(",", "."))
            elif positive:
                netto_eur_value = float(netto_eur)
            else:
                raise Exception()
            invoicing_currency.main_currency(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, today_pekao_rate_value)
        except ValueError:
            print("Proszę podać poprawną wartość.")
        except Exception:
            print("Wartość musi być większa od zera.")