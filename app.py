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

            # TESLA
            ("Tesla Model 3 SR", 1600000, 510, 25, 9, 8, 9, 9, 7, 7),
            ("Tesla Model 3 LR", 1850000, 602, 27, 9, 8, 9, 9, 7, 7),
            ("Tesla Model Y SR", 1750000, 533, 30, 9, 8, 9, 8, 7, 7),
            ("Tesla Model Y LR", 2000000, 565, 30, 9, 9, 9, 8, 7, 7),

            # TOGG
            ("TOGG T10X V1 RWD", 1450000, 523, 28, 8, 8, 8, 7, 7, 7),
            ("TOGG T10X V2 RWD", 1650000, 523, 26, 9, 9, 8, 8, 7, 7),

            # BMW
            ("BMW iX1", 1950000, 440, 29, 8, 9, 7, 8, 7, 7),
            ("BMW iX3", 2400000, 460, 32, 9, 9, 7, 8, 7, 7),
            ("BMW i4 eDrive40", 2450000, 590, 31, 9, 9, 8, 9, 8, 8),
            ("BMW i7", 4500000, 625, 34, 10, 10, 8, 9, 9, 9),

            # MERCEDES
            ("Mercedes EQA 250", 2100000, 426, 32, 8, 9, 7, 8, 7, 7),
            ("Mercedes EQB 250", 2250000, 423, 33, 8, 9, 7, 8, 7, 7),
            ("Mercedes EQE 350", 3200000, 590, 31, 9, 9, 8, 9, 8, 8),
            ("Mercedes EQS 450+", 4200000, 770, 35, 10, 10, 8, 9, 9, 9),

            # AUDI
            ("Audi Q4 e-tron", 2350000, 520, 31, 9, 9, 7, 8, 7, 7),
            ("Audi Q8 e-tron", 3100000, 582, 33, 9, 9, 7, 8, 8, 8),
            ("Audi e-tron GT", 4800000, 488, 28, 10, 9, 8, 9, 9, 9),

            # VOLKSWAGEN
            ("VW ID.3", 1650000, 426, 30, 7, 7, 7, 7, 6, 6),
            ("VW ID.4", 1800000, 520, 30, 8, 8, 7, 8, 7, 7),
            ("VW ID.5", 2000000, 514, 30, 8, 8, 7, 8, 7, 7),
            ("VW ID.7", 2300000, 620, 29, 9, 9, 7, 8, 8, 8),

            # HYUNDAI
            ("Hyundai Kona Electric", 1550000, 484, 27, 7, 7, 7, 7, 6, 6),
            ("Hyundai Ioniq 5", 1700000, 507, 26, 8, 8, 8, 8, 7, 7),
            ("Hyundai Ioniq 6", 1850000, 614, 24, 9, 8, 8, 9, 8, 8),

            # KIA
            ("Kia EV3", 1550000, 430, 27, 7, 7, 7, 7, 6, 6),
            ("Kia Niro EV", 1600000, 460, 28, 7, 7, 7, 7, 6, 6),
            ("Kia EV6", 1850000, 528, 24, 9, 8, 8, 9, 8, 8),
            ("Kia EV9", 2600000, 541, 32, 9, 9, 8, 8, 8, 8),

            # RENAULT
            ("Renault Megane E-Tech", 1550000, 450, 30, 8, 7, 7, 7, 7, 7),
            ("Renault Zoe", 1350000, 395, 34, 6, 6, 6, 6, 6, 6),
            ("Renault Scenic E-Tech", 1900000, 620, 28, 8, 8, 7, 7, 7, 7),

            # PEUGEOT
            ("Peugeot e-208", 1350000, 362, 32, 6, 6, 6, 6, 6, 6),
            ("Peugeot e-2008", 1500000, 345, 32, 6, 7, 6, 6, 6, 6),
            ("Peugeot e-308", 1650000, 412, 31, 7, 7, 6, 7, 7, 7),

            # OPEL
            ("Opel Corsa-e", 1350000, 357, 32, 6, 6, 6, 6, 6, 6),
            ("Opel Mokka-e", 1450000, 338, 33, 6, 7, 6, 6, 6, 6),
            ("Opel Astra Electric", 1650000, 418, 30, 7, 7, 6, 7, 7, 7),

            # FIAT
            ("Fiat 500e", 1350000, 320, 34, 6, 6, 6, 6, 6, 6),

            # MINI
            ("Mini Cooper SE", 1550000, 402, 29, 7, 7, 7, 8, 7, 7),

            # VOLVO
            ("Volvo EX30", 1700000, 476, 26, 8, 8, 8, 8, 8, 8),
            ("Volvo XC40 Recharge", 2250000, 418, 32, 8, 9, 7, 8, 8, 8),
            ("Volvo EX90", 3500000, 600, 33, 9, 10, 8, 8, 9, 9),

            # PORSCHE
            ("Porsche Taycan", 5200000, 484, 22, 10, 9, 9, 10, 9, 10),

            # FORD
            ("Ford Mustang Mach-E", 2300000, 610, 28, 8, 8, 7, 8, 7, 7),

            # SKODA
            ("Skoda Enyaq iV", 2000000, 545, 31, 8, 8, 7, 7, 7, 7),

            # CUPRA
            ("Cupra Born", 1750000, 424, 29, 8, 7, 7, 8, 7, 7),

            # NISSAN
            ("Nissan Leaf", 1400000, 385, 34, 6, 6, 6, 6, 6, 6),
            ("Nissan Ariya", 2200000, 533, 30, 8, 8, 7, 7, 7, 7),
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
