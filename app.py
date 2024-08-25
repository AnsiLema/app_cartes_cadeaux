import os
import stripe
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Clés API Stripe (remplacez-les par vos clés réelles)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  # Clé secrète Stripe
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')  # Clé publique Stripe

# Simuler une base de données de cartes-cadeaux
gift_cards = {
    "ABC123": {"expiration_date": datetime(2023, 8, 20)},
    "XYZ789": {"expiration_date": datetime(2024, 1, 15)},
    "GIFT456": {"expiration_date": datetime(2023, 12, 31)},
}

# Vérifier si une carte est expirée
def is_card_valid(card_code):
    card = gift_cards.get(card_code)
    if card:
        return datetime.now() <= card["expiration_date"]
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_card():
    card_code = request.form['card_code']
    if is_card_valid(card_code):
        return f"La carte {card_code} est valide."
    elif card_code in gift_cards:
        return redirect(url_for('reactivate_card', card_code=card_code))
    else:
        return "Carte inconnue."

@app.route('/reactivate/<card_code>')
def reactivate_card(card_code):
    return render_template('reactivate.html', card_code=card_code, public_key=STRIPE_PUBLIC_KEY)

@app.route('/pay', methods=['POST'])
def pay():
    card_code = request.form['card_code']
    # Créer une session de paiement Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': f"Réactivation de la carte {card_code}",
                },
                'unit_amount': 2000,  # 20 euros en centimes
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', card_code=card_code, _external=True),
        cancel_url=url_for('cancel', _external=True),
    )
    return redirect(session.url, code=303)

@app.route('/success/<card_code>')
def success(card_code):
    # Réactiver la carte après le succès du paiement
    if card_code in gift_cards:
        gift_cards[card_code]["expiration_date"] = datetime.now() + timedelta(days=365)
        return f"La carte {card_code} a été réactivée avec succès pour 1 an supplémentaire!"
    else:
        return "Erreur: Carte non trouvée."

@app.route('/cancel')
def cancel():
    return "Le paiement a été annulé."

if __name__ == '__main__':
    app.run(debug=True)
