# Invoices checker
This program matches the payment date with the correct NBP table and exchange rate.

I created this project to fasten my current job. 

Placing invoices with RAKS SQL works fine, but sometimes prices and exchange rates don't match, thus it is necessary to check if the calculation is correct. Before this project, I counted everything using the calculator, but I decided to optimize my job, and that's how this program started. The main problem with calculations was, that there is no option in RAKS SQL to match the payment date with the right NBP table by default (it should be the one released the day before the payment date). That is why I did it by myself using NBP API, BeautifulSoup for parsing the Pekao SA website (the source of exchange rates for calculations in PLN) and working on a text file containing previously downloaded NBP exchange rates.
