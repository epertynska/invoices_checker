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
    today_pekao_rate_value = float(all[-1].split()[1].rstrip("\n"))

# Main function in the program
invoice_net_value.netto(way_out.end, NBP_RATES_FILE, current_date, netto_eur_value, VAT, BRUTTO, DATE_FORMAT, PEKAO_RATES_FILE, today_pekao_rate_value)