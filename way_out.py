import invoice_net_value

end = False

def exit(NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, today_pekao_rate_value):
    global end
    end = True
    invoice_net_value.netto(end, NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, today_pekao_rate_value)