from flask import Flask, request, render_template_string
import sqlite3
import math

app = Flask(__name__)
DB = "cars.db"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS cars")

    c.execute("""
    CREATE TABLE cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        range_km INTEGER,
        charge_time INTEGER,
        multimedia INTEGER,
        comfort INTEGER,
        regen INTEGER,
        pedal INTEGER
    )
    """)

    cars = [

        # TESLA
        ("Tesla Model 3 SR", 1600000, 510, 25, 9, 8, 9, 9),
        ("Tesla Model 3 LR", 1850000, 602, 27, 9, 8, 9, 9),
        ("Tesla Model Y SR", 1750000, 533, 30, 9, 8, 9, 8),
        ("Tesla Model Y LR", 2000000, 565, 30, 9, 9, 9, 8),

        # TOGG
        ("TOGG T10X V1 RWD", 1450000, 523, 28, 8, 8, 8, 7),
        ("TOGG T10X V2 RWD", 1650000, 523, 26, 9, 9, 8, 8),

        # BMW
        ("BMW iX1", 1950000, 440, 29, 8, 9, 7, 8),
        ("BMW iX3", 2400000, 460, 32, 9, 9, 7, 8),
        ("BMW i4 eDrive40", 2450000, 590, 31, 9, 9, 8, 9),
        ("BMW i7", 4500000, 625, 34, 10, 10, 8, 9),

        # MERCEDES
        ("Mercedes EQA 250", 2100000, 426, 32, 8, 9, 7, 8),
        ("Mercedes EQB 250", 2250000, 423, 33, 8, 9, 7, 8),
        ("Mercedes EQE 350", 3200000, 590, 31, 9, 9, 8, 9),
        ("Mercedes EQS 450+", 4200000, 770, 35, 10, 10, 8, 9),

        # AUDI
        ("Audi Q4 e-tron", 2350000, 520, 31, 9, 9, 7, 8),
        ("Audi Q8 e-tron", 3100000, 582, 33, 9, 9, 7, 8),
        ("Audi e-tron GT", 4800000, 488, 28, 10, 9, 8, 9),

        # VOLKSWAGEN
        ("VW ID.3", 1650000, 426, 30, 7, 7, 7, 7),
        ("VW ID.4", 1800000, 520, 30, 8, 8, 7, 8),
        ("VW ID.5", 2000000, 514, 30, 8, 8, 7, 8),
        ("VW ID.7", 2300000, 620, 29, 9, 9, 7, 8),

        # HYUNDAI
        ("Hyundai Kona Electric", 1550000, 484, 27, 7, 7, 7, 7),
        ("Hyundai Ioniq 5", 1700000, 507, 26, 8, 8, 8, 8),
        ("Hyundai Ioniq 6", 1850000, 614, 24, 9, 8, 8, 9),

        # KIA
        ("Kia EV3", 1550000, 430, 27, 7, 7, 7, 7),
        ("Kia Niro EV", 1600000, 460, 28, 7, 7, 7, 7),
        ("Kia EV6", 1850000, 528, 24, 9, 8, 8, 9),
        ("Kia EV9", 2600000, 541, 32, 9, 9, 8, 8),

        # RENAULT
        ("Renault Megane E-Tech", 1550000, 450, 30, 8, 7, 7, 7),
        ("Renault Zoe", 1350000, 395, 34, 6, 6, 6, 6),
        ("Renault Scenic E-Tech", 1900000, 620, 28, 8, 8, 7, 7),

        # PEUGEOT
        ("Peugeot e-208", 1350000, 362, 32, 6, 6, 6, 6),
        ("Peugeot e-2008", 1500000, 345, 32, 6, 7, 6, 6),
        ("Peugeot e-308", 1650000, 412, 31, 7, 7, 6, 7),

        # OPEL
        ("Opel Corsa-e", 1350000, 357, 32, 6, 6, 6, 6),
        ("Opel Mokka-e", 1450000, 338, 33, 6, 7, 6, 6),
        ("Opel Astra Electric", 1650000, 418, 30, 7, 7, 6, 7),

        # FIAT
        ("Fiat 500e", 1350000, 320, 34, 6, 6, 6, 6),

        # MINI
        ("Mini Cooper SE", 1550000, 402, 29, 7, 7, 7, 8),

        # VOLVO
        ("Volvo EX30", 1700000, 476, 26, 8, 8, 8, 8),
        ("Volvo XC40 Recharge", 2250000, 418, 32, 8, 9, 7, 8),
        ("Volvo EX90", 3500000, 600, 33, 9, 10, 8, 8),

        # PORSCHE
        ("Porsche Taycan", 5200000, 484, 22, 10, 9, 9, 10),

        # FORD
        ("Ford Mustang Mach-E", 2300000, 610, 28, 8, 8, 7, 8),

        # SKODA
        ("Skoda Enyaq iV", 2000000, 545, 31, 8, 8, 7, 7),

        # CUPRA
        ("Cupra Born", 1750000, 424, 29, 8, 7, 7, 8),

        # NISSAN
        ("Nissan Leaf", 1400000, 385, 34, 6, 6, 6, 6),
        ("Nissan Ariya", 2200000, 533, 30, 8, 8, 7, 7),
    ]

    c.executemany("""
    INSERT INTO cars
    (name, price, range_km, charge_time,
     multimedia, comfort, regen, pedal)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, cars)

    conn.commit()
    conn.close()

# ================= LOGIC =================
def calculate_score(user, car):
    return (
        abs(user["multimedia"] - car["multimedia"]) +
        abs(user["comfort"] - car["comfort"]) +
        abs(user["regen"] - car["regen"]) +
        abs(user["pedal"] - car["pedal"])
    )

def explain(user, car):
    bullets = []

    def yakınlık(u, c):
        diff = abs(u - c)
        if diff == 0:
            return "birebir örtüşüyor"
        elif diff == 1:
            return "beklentine çok yakın"
        elif diff == 2:
            return "beklentine yakın"
        else:
            return "beklentinden uzak"

    bullets.append(f"• Gaz pedal hassasiyeti: {yakınlık(user['pedal'], car['pedal'])}.")
    bullets.append(f"• Rejenerasyon seviyesi: {yakınlık(user['regen'], car['regen'])}.")
    bullets.append(f"• Sürüş konforu: {yakınlık(user['comfort'], car['comfort'])}.")
    bullets.append(f"• Multimedya seviyesi: {yakınlık(user['multimedia'], car['multimedia'])}.")

    if car["price"] <= user["price"] and car["range_km"] >= user["range"]:
        bullets.append(
            f"• Fiyat ({car['price']} TL) ve menzil ({car['range_km']} km) kriterlerinle uyumlu."
        )

    return "<br>".join(bullets)

# ================= UI =================
HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Elektrikli Araç Öneri</title>
<style>
body { font-family: Arial; margin:40px; }
input[type=range] { width:320px; }
.card { border:1px solid #999; padding:20px; margin-top:20px; }
</style>

<script>
function show(id,val){
    document.getElementById(id).innerText = val + " / 10";
}
function showCharge(val){
    document.getElementById("chargeVal").innerText =
        (val == 61) ? "60+ dk" : val + " dk";
}
</script>

</head>
<body>

<h2>Elektrikli Araç Tercihleri</h2>

<form method="post">

Fiyat üst sınır (TL):<br>
<input type="number" name="price" required><br><br>

Minimum menzil (km):<br>
<input type="number" name="range" required><br><br>

Şarj süresi:
<b><span id="chargeVal">30 dk</span></b><br>
<input type="range" name="charge" min="1" max="61" value="30"
oninput="showCharge(this.value)">
<br><br>

Gaz pedal hassasiyeti:
<b><span id="pedalVal">5 / 10</span></b><br>
<input type="range" name="pedal" min="1" max="10" value="5"
oninput="show('pedalVal',this.value)">
<br><br>

Rejenerasyon seviyesi:
<b><span id="regenVal">5 / 10</span></b><br>
<input type="range" name="regen" min="1" max="10" value="5"
oninput="show('regenVal',this.value)">
<br><br>

Sürüş konforu:
<b><span id="comfortVal">5 / 10</span></b><br>
<input type="range" name="comfort" min="1" max="10" value="5"
oninput="show('comfortVal',this.value)">
<br><br>

Multimedya:
<b><span id="multimediaVal">5 / 10</span></b><br>
<input type="range" name="multimedia" min="1" max="10" value="5"
oninput="show('multimediaVal',this.value)">
<br><br>

<button>Aracı Öner</button>
</form>

{% if car %}
<div class="card">
<h3>{{car.name}}</h3>
<p>{{explanation|safe}}</p>
</div>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    car = None
    explanation = ""

    if request.method == "POST":
        charge_val = int(request.form["charge"])
        user_charge = 60 if charge_val == 61 else charge_val

        user = {
            "price": int(request.form["price"]),
            "range": int(request.form["range"]),
            "charge": user_charge,
            "pedal": int(request.form["pedal"]),
            "regen": int(request.form["regen"]),
            "comfort": int(request.form["comfort"]),
            "multimedia": int(request.form["multimedia"]),
        }

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM cars")
        rows = c.fetchall()
        conn.close()

        best = None
        best_score = math.inf

        for r in rows:
            car_data = {
                "name": r[1],
                "price": r[2],
                "range_km": r[3],
                "charge": r[4],
                "multimedia": r[5],
                "comfort": r[6],
                "regen": r[7],
                "pedal": r[8],
            }

            if car_data["price"] > user["price"]:
                continue
            if car_data["range_km"] < user["range"]:
                continue
            if car_data["charge"] > user["charge"]:
                continue

            s = calculate_score(user, car_data)
            if s < best_score:
                best_score = s
                best = car_data

        if best:
            car = best
            explanation = explain(user, best)

    return render_template_string(HTML, car=car, explanation=explanation)

import webbrowser

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
