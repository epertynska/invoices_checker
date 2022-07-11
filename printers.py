# print the calculations in EUR
def printer_eur(netto_eur, tabela, kurs, VAT, BRUTTO, rate_date):
    print("\nNumer tabeli kursowej:", tabela)
    print("Data emisji tabeli kursowej:", rate_date)
    print("Kurs:", kurs)
    print(f"""
          Wartość netto EUR: {str(round(netto_eur, 2)).replace(".", ",")} €

          Wartość netto PLN: {str(round(netto_eur * kurs, 2)).replace(".", ",")} PLN

          Wartość VAT PLN: {str(round(netto_eur * kurs * VAT, 2)).replace(".", ",")} PLN

          Wartość brutto EUR: {str(round(netto_eur * BRUTTO, 2)).replace(".", ",")} €
          """)

# print the calculations in PLN
def printer_pln(netto_eur, kurs, date, VAT, BRUTTO):
    print("\nKurs sprzedaży Pekao SA opublikowany {} o godzinie 7:00 wynosi {}".format(date, kurs))
    print(f"""
        Wartość netto PLN: {str(round(netto_eur * kurs, 2)).replace(".", ",")} PLN

        Wartość VAT PLN: {str(round(netto_eur * kurs * VAT, 2)).replace(".", ",")} PLN

        Wartość brutto PLN: {str(round(netto_eur * kurs * BRUTTO, 2)).replace(".", ",")} PLN
        """)