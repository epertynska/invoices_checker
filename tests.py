import datetime

ok_test = True
msg = ""
# dictionary of bank holidays in 2022
bank_holidays_2022 = {"2022-01-06": "Święto Trzech Króli", "2022-04-18": "drugi dzień Wielkiej Nocy", "2022-05-03": "Święto Narodowe Konstytucji 3 Maja", "2022-06-16": "Boże Ciało", "2022-08-15": "Wniebowzięcie Najświętszej Maryi Panny, Święto Wojska Polskiego", "2022-11-01": "Wszystkich Świętych", "2022-11-11": "Narodowe Święto Niepodległości", "2022-12-26": "drugi dzień Bożego Narodzenia"}

# checking if date is given in the right format and length
def test_format(payment):
    global ok_test, msg
    check = payment.split("-")
    test_check = len(check) == 3
    if not test_check or not check:
        msg += "Powinna się składać z 3 liczb oddzielonych myślnikami.\n"
        ok_test = False
    return msg, ok_test

# checking if given date contains only numbers and "-"
def test_digits(payment):
    global ok_test, msg
    signs = ("1234567890-")
    nums_bools = [num for num in payment if num in signs]
    test_nums = len(nums_bools) == 10
    if not test_nums:
        msg += "Data powinna się składać z cyfr i myślników.\n"
        ok_test = False
    return msg, ok_test

# testing if given data is in YYYY-MM-DD format
def test_length(payment):
    global ok_test, msg
    check = payment.split("-")
    if len("".join(check)) == 8:
        test_length = len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2 
    else:
        test_length = False
    if not test_length or not check:
        msg += "Data powinna być wpisana w systemie 4-2-2.\n"
        ok_test = False
    return msg, ok_test

# test of given data existence
def test_real(payment,current_date):
    global ok_test, msg
    check = payment.split("-")
    if len("".join(check)) == 8:
        test_date = int(check[0]) <= int(str(current_date).split("-")[0]) and (int(check[1]) > 0 and int(check[1]) <= 12) and (int(check[2]) > 0 and int(check[2]) <= 31)
    else:
        test_date = False
    if not test_date or not check:
        msg += "Taka data nie istnieje.\n"
        ok_test = False
    return msg, ok_test

# weekend days check
def test_weekend(payment, current_date, DATE_FORMAT):
    global ok_test, msg
    given_date = datetime.datetime.strptime(payment, DATE_FORMAT)
    test_weekend = datetime.datetime.weekday(given_date) <= 4
    if not test_weekend:
        msg += "Podany dzień przypada na weekend.\n"
        ok_test = False
    return msg, ok_test

# check if date isn't in the future
def test_future(payment, DATE_FORMAT, current_date): 
    global ok_test, msg
    given_date = datetime.datetime.strptime(payment, DATE_FORMAT)   
    current = datetime.datetime.strptime(current_date, DATE_FORMAT)
    test_f = given_date <= current
    if not test_f:
        msg += "Podany dzień jeszcze nie nastąpił.\n"
        ok_test = False
    return msg, ok_test

# bank holidays check
def test_holidays(payment):
    global ok_test, msg
    test_bank_holiday = payment not in bank_holidays_2022
    if not test_bank_holiday:
        msg += "\nTen dzień to {}.".format(bank_holidays_2022[payment])
        ok_test = False
    return msg, ok_test