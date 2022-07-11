import tests, euro_rates, pekao_rates, way_out

# taking date of payment
def date_input(currency, NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE):
    while True:
        payment = input("Podaj datę wpływu na konto: (RRRR-MM-DD)\n")
        msg_1 = "Data jest niepoprawna.\n"
        if tests.ok_test is True:
            tests.test_format(payment)
        if tests.ok_test is True:
            tests.test_digits(payment)
        if tests.ok_test is True:
            tests.test_length(payment)
        if tests.ok_test is True:
            tests.test_real(payment, current_date)
        if tests.ok_test is True:
            tests.test_weekend(payment, current_date, DATE_FORMAT)
        if tests.ok_test is True:
            tests.test_future(payment, DATE_FORMAT, current_date)
        if tests.ok_test is True:
            tests.test_holidays(payment)

      
        if tests.msg == "":
            if currency == "EUR":
                euro_rates.euro_rate_for_payment(payment, NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO)
                break
            else:
                pekao_rates.today_pekao_rate(payment, PEKAO_RATES_FILE, netto_eur_value, VAT, BRUTTO)
                break
        elif payment == "q":
            way_out.exit(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, pekao_rates.today_pekao_rate_value)
            break
        else:
            print(msg_1 + tests.msg)
            tests.msg = ""
            tests.ok_test = True