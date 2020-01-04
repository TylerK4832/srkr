
import os
import sqlite3

from flask import Flask, render_template, request, make_response, redirect

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
    ids=[]
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
            ids.append(rentals[i][5])
            length+=1
    return render_template("rent.html", names=names, descriptions=descriptions, types=types, costs_hour=costs_hour, costs_day=costs_day, length=length, ids=ids)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method=="GET":
        if 'cart_items' in request.cookies:
            connection=sqlite3.connect("rentals.db")
            cursor=connection.cursor()
            cursor.execute("SELECT * FROM rentals")
            rentals=cursor.fetchall()
            names=[]
            costs_hour=[]
            costs_day=[]
            ids=[]
            for i in range(len(rentals)):
                names.append(rentals[i][0])
                costs_hour.append(rentals[i][3])
                costs_day.append(rentals[i][4])
                ids.append(rentals[i][5])
            item_list=[]
            name_list=[]
            quantity_list=[]
            cost_hour_list=[]
            cost_day_list=[]
            cookie=str(request.cookies.get('cart_items'))
            the_list=cookie.split()
            for i in range(len(the_list)):
                item_list.append(int(the_list[i][0:3]))
                quantity_list.append(int(the_list[i][4:]))
            length=len(the_list)
            for i in range(len(the_list)):
                name_list.append(names[ids.index(item_list[i])])
                cost_hour_list.append(costs_hour[ids.index(item_list[i])])
                cost_day_list.append(costs_day[ids.index(item_list[i])])
            return render_template("cart.html", name_list=name_list, cost_hour_list=cost_hour_list, cost_day_list=cost_day_list, quantity_list=quantity_list, length=length)
        else:
            return render_template("cart.html")

    if request.method=="POST":
        new_item=(str(request.form.get("item"))+":"+str(request.form.get("quantity"))+" ")
        if 'cart_items' in request.cookies:
            new_cookie=str(request.cookies.get('cart_items'))+str(new_item)
        else:
            new_cookie=str(new_item)
        response = make_response(render_template("cart.html"))
        response.set_cookie('cart_items', new_cookie)
        return response
        return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
