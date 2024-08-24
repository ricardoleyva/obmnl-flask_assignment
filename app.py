# Import libraries
from flask import Flask, request, redirect, url_for, render_template

# Instantiate Flask functionality
app = Flask("Transaction records")

# Sample data
transactions = [
    {"id": 1, "date": "2023-06-01", "amount": 100},
    {"id": 2, "date": "2023-06-02", "amount": -200},
    {"id": 3, "date": "2023-06-03", "amount": 300},
]


# Read operation
@app.route("/")
@app.route("/index")
@app.route("/home")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Search operation
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min = float(request.form["min_amount"])
        max = float(request.form["max_amount"])
        filtered_transactions = [
            transaction
            for transaction in transactions
            if (transaction["amount"] >= min and transaction["amount"] <= max)
        ]
        # filtered_transactions = []
        # for transaction in transactions:
        #    if (transaction["amount"] >= min and transaction["amount"] <= max):
        #        filtered_transactions.append(transaction)
        return render_template("transactions.html", transactions=filtered_transactions)
    return render_template("search.html")


# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        id = len(transactions) + 1
        date = request.form["date"]
        amount = float(request.form["amount"])
        transactions.append({"id": id, "date": date, "amount": amount})
        return redirect(url_for("get_transactions"))
    return render_template("form.html")


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = date
                transaction["amount"] = amount
                break
        return redirect(url_for("get_transactions"))
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)
    return ({"message": "Transaction not found"}, 404)


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))


# Balance
@app.route("/balance")
def total_balance():
    balance = 0
    balance_flag = False
    for transaction in transactions:
        balance += transaction["amount"]
    if balance > 0:
        balance_flag = True
    total_amount = f"Total Balance: {balance}"
    return render_template(
        "transactions.html",
        transactions=transactions,
        total_amount=total_amount,
        balance_flag=balance_flag,
    )


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
