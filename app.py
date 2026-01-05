import sqlite3
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
DB_NAME = "cars.db"


# -------------------- DATABASE --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        range_km INTEGER,
        charge_time INTEGER,
        pedal INTEGER,
        regen INTEGER,
        comfort INTEGER,
        multimedia INTEGER,
        seat INTEGER,
        material INTEGER
    )
    """)

    c.execute("SELECT COUNT(*) FROM cars")
    if c.fetchone()[0] == 0:
        cars = [
            ("Tesla Model 3", 1600000, 510, 30, 9, 9, 8, 9, 8, 8),
            ("Tesla Model Y", 1900000, 530, 32, 9, 8, 9, 9, 9, 8),
            ("Togg T10X", 1450000, 523, 28, 7, 7, 8, 8, 8, 7),
            ("BMW i4", 2500000, 590, 35, 8, 8, 9, 9, 9, 9),
            ("Mercedes EQE", 3000000, 550, 40, 7, 7, 9, 9, 9, 9),
            ("Hyundai Kona EV", 1400000, 484, 45, 7, 7, 7, 7, 7, 7),
            ("Kia EV6", 1800000, 528, 38, 8, 8, 8, 8, 8, 8)
        ]

        c.executemany("""
        INSERT INTO cars
        (name, price, range_km, charge_time, pedal, regen, comfort, multimedia, seat, material)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, cars)

    conn.commit()
    conn.close()


# -------------------- SCORING --------------------
def score(car, user):
    score = 0
    explanations = []

    def closeness(label, car_val, user_val):
        diff = abs(car_val - user_val)
        if diff <= 1:
            return f"• {label}: beklentine çok yakın."
        elif diff <= 3:
            return f"• {label}: beklentine yakın."
        else:
            return f"• {label}: beklentinden uzak."

    explanations.append(closeness("Gaz pedal hassasiyeti", car["pedal"], user["pedal"]))
    explanations.append(closeness("Rejenerasyon seviyesi", car["regen"], user["regen"]))
    explanations.append(closeness("Sürüş konforu", car["comfort"], user["comfort"]))
    explanations.append(closeness("Multimedya seviyesi", car["multimedia"], user["multimedia"]))
    explanations.append(closeness("Koltuk rahatlığı", car["seat"], user["seat"]))
    explanations.append(closeness("İç malzeme kalitesi", car["material"], user["material"]))

    if car["price"] <= user["price"] and car["range_km"] >= user["range"]:
        explanations.append(
            f"• Fiyat ({car['price']} TL) ve menzil ({car['range_km']} km) kriterlerinle uyumlu."
        )

    score += max(0, user["price"] - car["price"]) / 10000
    score += max(0, car["range_km"] - user["range"])
    score += sum(10 - abs(car[k] - user[k]) for k in ["pedal", "regen", "comfort", "multimedia", "seat", "material"])

    return score, explanations


# -------------------- ROUTE --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user = {
            "price": int(request.form["price"]),
            "range": int(request.form["range"]),
            "charge": int(request.form["charge"]),
            "pedal": int(request.form["pedal"]),
            "regen": int(request.form["regen"]),
            "comfort": int(request.form["comfort"]),
            "multimedia": int(request.form["multimedia"]),
            "seat": int(request.form["seat"]),
            "material": int(request.form["material"])
        }

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM cars")
        rows = c.fetchall()
        conn.close()

        cars = []
        for r in rows:
            cars.append({
                "name": r[1], "price": r[2], "range_km": r[3], "charge_time": r[4],
                "pedal": r[5], "regen": r[6], "comfort": r[7],
                "multimedia": r[8], "seat": r[9], "material": r[10]
            })

        best = None
        best_score = -1
        best_exp = []

        for car in cars:
            s, e = score(car, user)
            if s > best_score:
                best_score = s
                best = car
                best_exp = e

        result = {"car": best, "exp": best_exp}

    return render_template_string(HTML, result=result)


# -------------------- HTML --------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Elektrikli Araç Öneri Sistemi</title>
<style>
body { font-family: Arial; max-width: 800px; margin: auto; }
label { display:block; margin-top:15px; }
</style>
</head>
<body>

<h2>Elektrikli Araç Öneri Sistemi</h2>

<form method="POST">
<label>Max Fiyat (TL)</label>
<input type="number" name="price" required>

<label>Minimum Menzil (km)</label>
<input type="number" name="range" required>

<label>Şarj Süresi (dk, 1–60+)</label>
<input type="range" name="charge" min="1" max="60" value="30"
oninput="this.nextElementSibling.value=this.value"><output>30</output>

{% for name,label in [
("pedal","Gaz Pedal Hassasiyeti"),
("regen","Rejenerasyon Seviyesi"),
("comfort","Sürüş Konforu"),
("multimedia","Multimedya"),
("seat","Koltuk Rahatlığı"),
("material","İç Malzeme Kalitesi")
] %}
<label>{{label}} (1–10)</label>
<input type="range" name="{{name}}" min="1" max="10" value="5"
oninput="this.nextElementSibling.value=this.value"><output>5</output>
{% endfor %}

<br><br>
<button type="submit">Araç Öner</button>
</form>

{% if result %}
<hr>
<h3>{{result.car.name}}</h3>
<ul>
{% for e in result.exp %}
<li>{{e}}</li>
{% endfor %}
</ul>
{% endif %}

</body>
</html>
"""

# -------------------- START --------------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
