
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

@app.route("/rent/")
@app.route("/rent/<type>/")
def rent(type=1):
    connection=sqlite3.connect("rentals.db")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM rentals")
    rentals=cursor.fetchall()
    names=[]
    descriptions=[]
    types=[]
    costs_hour=[]
    costs_day=[]
    length=0
    type_indicator=-1
    if type=="kayak":
        type_indicator=1
    if type=="canoe":
        type_indicator=2
    if type=="paddleboard":
        type_indicator=3
    for i in range(len(rentals)):
        if type_indicator==rentals[i][2] or type_indicator==-1:
            names.append(rentals[i][0])
            descriptions.append(rentals[i][1])
            types.append(rentals[i][2])
            costs_hour.append(rentals[i][3])
            costs_day.append(rentals[i][4])
            length+=1
    return render_template("rent.html", names=names, descriptions=descriptions, types=types, costs_hour=costs_hour, costs_day=costs_day, length=length)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
