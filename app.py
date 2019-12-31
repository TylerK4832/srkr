
import os
import sqlite3

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/rent")
def rent():
    connection = sqlite3.connect("rentals.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM rentals")
    rentals=cursor.fetchall()
    names=[]
    descriptions=[]
    types=[]
    costs_hour=[]
    costs_day=[]
    length=len(rentals)
    for i in range(length):
        names.append(rentals[i][0])
        descriptions.append(rentals[i][1])
        types.append(rentals[i][2])
        costs_hour.append(rentals[i][3])
        costs_day.append(rentals[i][4])
    return render_template("rent.html", names=names, descriptions=descriptions, types=types, costs_hour=costs_hour, costs_day=costs_day, length=length)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
