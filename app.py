from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Simuler une base de données
cartes_cadeaux = {
    "ABC123": {"date_expiration": datetime(2023, 8, 20)},
    "XYZ789": {"date_expiration": datetime(2024, 1, 15)},
    "GIFT456": {"date_expiration": datetime(2023, 12, 31)},
}

def is_card_valid(card_code):
    card = cartes_cadeaux.get(card_code)
    if card:
        return datetime.now() <= card["date_expiration"]
    return False
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify_card():
    card_code = request.form["card_code"]
    if is_card_valid(card_code):
        return f"La carte {card_code} est valide."
    elif card_code in cartes_cadeaux:
        return redirect(url_for("reactivate_card", card_code=card_code))
    else:
        return "Carte inconnue."

@app.route("/reactivate_card/<card_code")
def reactivate_card(card_code):
    return render_template("reactivate.html", card_code=card_code)

@app.route('/pay', methods=['POST'])
def pay():
    card_code = request.form['card_code']
    # Simuler le paiement ici
    if card_code in cartes_cadeaux:
        # Réactiver la carte (on ajoute 1 an à la date d'expiration)
        cartes_cadeaux[card_code]["expiration_date"] = datetime.now() + timedelta(days=365)
        return f"La carte {card_code} a été réactivée avec succès pour 1 an supplémentaire!"
    else:
        return "Erreur: Carte non-trouvée."



if __name__ == '__main__':
    app.run(debug=True)
