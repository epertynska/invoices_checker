# Invoices checker

To be able to run this program, make sure to install:

- `pip install beautifulsoup4`
- `pip install requests`
- `pip install lxml`

You are welcome to use replit and see, how it works as well: [Invoices Checker]([https://replit.com/@EwaPertynska/invoices-bs4-json#main.py]).

This program matches the payment date with the correct NBP table and exchange rate, and also gets the Pekao SA sale exchange rate emitted at 7:00 on a given date.

I created this project to fasten my current job. 

Placing invoices with RAKS SQL works fine, but sometimes prices and exchange rates don't match, thus it is necessary to check if the calculation is correct. Before this project, I counted everything using the calculator, but I decided to optimize my job, and that's how this program started. The main problem with calculations was, that there is no option in RAKS SQL to match the payment date with the right NBP table by default (it should be the one released the day before the payment date). That is why I did it by myself using NBP API (json), BeautifulSoup for parsing the Pekao SA website (the source of exchange rates for calculations in PLN), and working on a text file containing previously downloaded exchange rates. Pekao SA rates file has been created using iteration over dates with datetime module.
