from flask import Flask, request, jsonify
from flask_cors import CORS  # Importera CORS
import sqlite3
import os

# Skapa Flask-appen
app = Flask(__name__)
CORS(app)  # Aktivera CORS för hela appen

# Databasens filnamn
DB_NAME = "transactions.db"

# Initialisera databasen
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 description TEXT,
                 amount REAL,
                 suggested_account TEXT)''')
    conn.commit()
    conn.close()

# Test-route för att verifiera att servern körs
@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route is working!"})

# Route för att lägga till en transaktion
@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    try:
        data = request.json
        description = data.get("description", "").strip()
        amount = data.get("amount", 0)

        if not description or amount <= 0:
            return jsonify({"error": "Invalid data provided"}), 400

        # Föreslå BAS-konto baserat på beskrivning
        if "mat" in description.lower():
            suggested_account = "4010 - Matinköp"
        elif "hyra" in description.lower():
            suggested_account = "5010 - Lokalhyra"
        else:
            suggested_account = "2999 - Övrigt"

        # Lägg till transaktionen i databasen
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO transactions (description, amount, suggested_account) VALUES (?, ?, ?)",
                  (description, amount, suggested_account))
        conn.commit()
        conn.close()

        return jsonify({"message": "Transaction added!", "suggested_account": suggested_account})
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# Route för att hämta alla transaktioner
@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    conn.close()

    # Formatera datan som en lista av objekt
    transactions_list = [
        {
            "id": row[0],
            "description": row[1],
            "amount": row[2],
            "suggested_account": row[3]
        }
        for row in transactions
    ]

    return jsonify({"transactions": transactions_list})

# Kör servern
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))  # Använd Render-port eller standardport 5000
    app.run(host='0.0.0.0', port=port, debug=True)
