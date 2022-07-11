import datetime
import update_rate_files

# checking if the "tabele_kursowe.txt" file is up to date
def file_check_nbp(NBP_RATES_FILE, DATE_FORMAT, current_date, today_nbp_table_no):
    delta = datetime.timedelta(days=1)
    with open(NBP_RATES_FILE, "r") as t:
        last = t.readlines()[-1].split()
        last_table = last[0].split("/")[0]
        date_last = last[1]
        start_date = str(datetime.datetime.strptime(date_last, DATE_FORMAT) + delta).split()[0]
        if today_nbp_table_no != last_table:
            update_rate_files.fill_eur_gap(start_date, current_date, NBP_RATES_FILE)
        else:
            print("Plik z tabelami kursowymi NBP jest aktualny.")
        return

# checking if the "kursy_pekao.txt" file is up to date
def file_check_pekao(PEKAO_RATES_FILE, current_date, DATE_FORMAT):
    with open(PEKAO_RATES_FILE, "r") as t:
        all = t.readlines()
        if all[-1].split()[0] != current_date:
            update_rate_files.fill_pln_gap(all[-1].split()[0], current_date, DATE_FORMAT, PEKAO_RATES_FILE)
        else:
            print("Plik z kursami Pekao jest aktualny.")
