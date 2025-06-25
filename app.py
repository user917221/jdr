from flask import Flask, request, render_template
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
import requests

app = Flask(__name__)

def get_coords(ville, username):
    url = f"http://api.geonames.org/searchJSON?q={ville}&maxRows=1&username={username}"
    response = requests.get(url)
    data = response.json()
    if not data["geonames"]:
        raise Exception("Ville introuvable.")
    geo = data["geonames"][0]
    return float(geo["lat"]), float(geo["lng"])

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        ville = request.form["ville"]
        date_naissance = request.form["date_naissance"]
        heure_naissance = request.form["heure_naissance"]
        username = request.form["username"]

        try:
            lat, lon = get_coords(ville, username)
            dt = Datetime(date_naissance, heure_naissance, '+00:00')
            pos = GeoPos(lat, lon)
            chart = Chart(dt, pos)
            asc = chart.get('ASC').sign

            result = f"Ascendant de {prenom} {nom} : {asc}"
        except Exception as e:
            result = f"Erreur : {str(e)}"

    return render_template("index.html", result=result)
