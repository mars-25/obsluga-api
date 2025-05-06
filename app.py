from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Pobranie kursów walut z API NBP
def get_exchange_rates():
    url = "http://api.nbp.pl/api/exchangerates/tables/C?format=json"
    response = requests.get(url)
    data = response.json()
    return {rate["code"]: rate["ask"] for rate in data[0]["rates"]}

#exchange_rates = get_exchange_rates() # Pobranie kursów przy starcie aplikacji

@app.route("/", methods=["GET", "POST"])
def index():
    exchange_rates = get_exchange_rates() #Pobieranie kursów za każdym razem ALE CZY NIE TRZEBA ODŚWIEŻYĆ STRONY?

    total_pln = None

    if request.method == "POST":
        currency = request.form.get("currency")  # Wybrana waluta
        amount = float(request.form.get("amount"))  # Ilość waluty

        if currency in exchange_rates:
            total_pln = round(amount * exchange_rates[currency], 2)  # Przeliczenie na PLN

    return render_template("index.html", exchange_rates=exchange_rates, total_pln=total_pln)

if __name__ == "__main__":
    app.run(debug=True)
