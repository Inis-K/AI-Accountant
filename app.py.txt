from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "transactions.db"

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

@app.route('/')
def home():
    return "AI Accountant Backend is running!"

@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    data = request.json
    description = data.get("description")
    amount = data.get("amount")

    if "mat" in description.lower():
        suggested_account = "4010 - Matinköp"
    elif "hyra" in description.lower():
        suggested_account = "5010 - Lokalhyra"
    else:
        suggested_account = "2999 - Övrigt"

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO transactions (description, amount, suggested_account) VALUES (?, ?, ?)",
              (description, amount, suggested_account))
    conn.commit()
    conn.close()

    return jsonify({"message": "Transaction added!", "suggested_account": suggested_account})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    conn.close()

    return jsonify({"transactions": transactions})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
