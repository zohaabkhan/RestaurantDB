from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "I am a secret key"

DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "admin"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route("/")
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM employees"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template("index.html", list_users=list_users)


@app.route("/add_employee", methods=["POST"])
def add_employee():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        ssn = request.form["ssn"]
        cur.execute(
            "INSERT INTO employees (fname, lname, email, phone, ssn) VALUES (%s,%s,%s,%s,%s)",
            (fname, lname, email, phone, ssn),
        )
        conn.commit()
        flash("Employee Added successfully")
        return redirect(url_for("Index"))


@app.route("/edit/<id>", methods=["POST", "GET"])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM employees WHERE id = %s", (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template("edit.html", Employee=data[0])


@app.route("/update/<id>", methods=["POST"])
def update_employee(id):
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        ssn = request.form["ssn"]

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE employees
            SET fname = %s,
                lname = %s,
                email = %s,
                phone = %s,
                ssn = %s
            WHERE id = %s
        """,
            (fname, lname, email, phone, ssn, id),
        )
        flash("Employee Updated Successfully")
        conn.commit()
        return redirect(url_for("Index"))


@app.route("/delete/<string:id>", methods=["POST", "GET"])
def delete_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("DELETE FROM employees WHERE id = {0}".format(id))
    conn.commit()
    flash("Employee Removed Successfully")
    return redirect(url_for("Index"))

@app.route("/shift")
def shift():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    q = "SELECT * FROM shift"
    cur.execute(q)  # Execute the SQL
    list_shifts = cur.fetchall()
    return render_template("shift.html", list_shifts=list_shifts)

@app.route("/add_shift", methods=["POST"])
def add_shift():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        employeeIDS = request.form["employeeIDS"]
        date = request.form["date"]
        
        cur.execute(
            "INSERT INTO shift (employeeIDS, date) VALUES (%s,%s)",
            (employeeIDS, date),
        )
        conn.commit()
        flash("Shift Added successfully")
        return redirect(url_for("shift"))

@app.route("/customer")
def customer():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    q = "SELECT * FROM customer"
    cur.execute(q)  # Execute the SQL
    list_customers = cur.fetchall()
    return render_template("customer.html", list_customers=list_customers)

@app.route("/add_customer", methods=["POST"])
def add_customer():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        customerFN = request.form["customerFN"]
        customerLN = request.form["customerLN"]
        phoneNumber = request.form["phoneNumber"]
        
        cur.execute(
            "INSERT INTO customer (customerFN, customerLN, phoneNumber) VALUES (%s,%s,%s)",
            (customerFN, customerLN, phoneNumber),
        )
        conn.commit()
        flash("Customer Added successfully")
        return redirect(url_for("customer"))

@app.route("/billing")
def billing():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    q = "SELECT * FROM billing"
    cur.execute(q)  # Execute the SQL
    list_bills = cur.fetchall()
    return render_template("billing.html", list_bills=list_bills)

@app.route("/add_billing", methods=["POST"])
def add_billing():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        transAmmount = request.form["transAmmount"]
        paymentType = request.form["paymentType"]
        
        cur.execute(
            "INSERT INTO billing (transAmmount, paymentType) VALUES (%s,%s)",
            (transAmmount, paymentType),
        )
        conn.commit()
        flash("Billing Added successfully")
        return redirect(url_for("billing"))

@app.route("/menu")
def menu():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    q = "SELECT * FROM menu"
    cur.execute(q)  # Execute the SQL
    list_menu = cur.fetchall()
    return render_template("menu.html", list_menu=list_menu)

@app.route("/add_menu", methods=["POST"])
def add_menu():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        menuDescription = request.form["menuDescription"]
        menuItem = request.form["menuItem"]

        cur.execute(
            "INSERT INTO menu (menuItem,menuDescription) VALUES (%s, %s)",
            (menuItem, menuDescription),
        )
        conn.commit()
        flash("Menu Description Added successfully")
        return redirect(url_for("menu"))

@app.route("/menuItem")
def menuItem():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    z = "SELECT * FROM menuItem"
    cur.execute(z)  # Execute the SQL
    list_menuItem = cur.fetchall()
    return render_template("menuItem.html", list_menuItem=list_menuItem)

@app.route("/add_menu", methods=["POST"])
def add_menuItem():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        menuPrice = request.form["menuPrice"]
        menuItemName = request.form["menuItemName"]
        menuItemQuantity = request.form["menuItemQuantity"]

        cur.execute(
            "INSERT INTO menu (menuPrice,menuItemName, menuItemQuantity) VALUES (%s, %s, %s)",
            (menuPrice, menuItemName, menuItemQuantity),
        )
        conn.commit()
        flash("Menu Price Added successfully")
        return redirect(url_for("menuItem"))

@app.route("/order")
def order():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    l = "SELECT * FROM orders"
    cur.execute(l)  # Execute the SQL
    list_order = cur.fetchall()
    return render_template("order.html", list_order=list_order)

@app.route("/add_order", methods=["POST"])
def add_order():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        orderItemQuantity = request.form["orderItemQuantity"]
        orderDate = request.form["orderDate"]

        cur.execute(
            "INSERT INTO orders (orderItemQuantity,orderDate) VALUES (%s, %s)",
            (orderItemQuantity, orderDate),
        )
        conn.commit()
        flash("Order Added successfully")
        return redirect(url_for("order"))

if __name__ == "__main__":
    app.run(debug=True)
