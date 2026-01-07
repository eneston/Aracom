import sqlite3
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
DB_NAME = "cars_full_system.db"


# -------------------- DATABASE (TÜM LİSTE EKSİKSİZ) --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS cars")
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

    # Senin verdiğin listenin tamamı (Hiçbir model çıkarılmadı)
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

    c.executemany(
        "INSERT INTO cars (name, price, range_km, charge_time, pedal, regen, comfort, multimedia, seat, material) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        cars)
    conn.commit()
    conn.close()


# -------------------- SCORING (ALGORİTMA) --------------------
def calculate_score(car, user):
    # Kritik Filtreler
    if car["price"] > user["price"]:
        return None, "Bütçeniz yetersiz."
    if car["range_km"] < user["range"]:
        return None, "Menzili beklentinizin altında."

    score = 0
    # Fiyat avantajı (Bütçeden kalan her 10.000 TL için 1 puan)
    score += (user["price"] - car["price"]) / 10000
    # Menzil avantajı (Her fazla km için 1 puan)
    score += (car["range_km"] - user["range"])
    # Şarj süresi (Her dakika sapma için -10 puan)
    score -= abs(car["charge_time"] - user["charge"]) * 10

    # Kişisel tercihler (1-10 arası özellikler)
    attrs = ["pedal", "regen", "comfort", "multimedia", "seat", "material"]
    for attr in attrs:
        score += (10 - abs(car[attr] - user[attr])) * 10

    return score


# -------------------- ROUTES --------------------
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
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM cars").fetchall()
        conn.close()

        best_car = None
        best_score = -999999

        for r in rows:
            car = dict(r)
            s = calculate_score(car, user)
            if s is not None and isinstance(s, (int, float)):
                if s > best_score:
                    best_score = s
                    best_car = car

        if best_car:
            result = {"car": best_car, "status": "success"}
        else:
            result = {"status": "error", "msg": "Kriterlere uygun araç bulunamadı."}

    return render_template_string(HTML, result=result)


# -------------------- HTML / CSS / JS --------------------
HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>EV Bulucu - Pro</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; margin: 0; padding: 20px; color: #1a1a1a; }
        .container { max-width: 650px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #007bff; margin-bottom: 30px; }
        .input-group { margin-bottom: 20px; }
        label { display: block; font-weight: 600; margin-bottom: 8px; font-size: 14px; }
        input[type="number"] { width: 100%; padding: 12px; border: 2px solid #e1e4e8; border-radius: 10px; font-size: 16px; outline: none; transition: 0.3s; }
        input[type="number"]:focus { border-color: #007bff; }

        .slider-wrapper { display: flex; align-items: center; gap: 15px; }
        input[type="range"] { flex: 1; accent-color: #007bff; }
        .val-badge { background: #007bff; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; }

        button { width: 100%; background: #007bff; color: white; border: none; padding: 18px; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 30px; box-shadow: 0 5px 15px rgba(0,123,255,0.3); transition: 0.3s; }
        button:hover { background: #0056b3; transform: translateY(-2px); }

        .result { margin-top: 40px; padding: 25px; border-radius: 15px; background: #f8f9fa; border: 2px solid #007bff; }
        .error { margin-top: 40px; padding: 25px; border-radius: 15px; background: #fff5f5; border: 2px solid #ff4d4d; color: #d63031; text-align: center; }
        .spec-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e1e4e8; }
        .spec-label { color: #636e72; font-weight: 500; }
        .spec-val { font-weight: bold; color: #2d3436; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ EV Danışmanı</h1>
        <form method="POST">
            <div class="input-group">
                <label>Maksimum Bütçe (TL)</label>
                <input type="number" name="price" value="1800000" placeholder="Örn: 2000000" required>
            </div>

            <div class="input-group">
                <label>Minimum Menzil (km)</label>
                <input type="number" name="range" value="400" placeholder="Örn: 450" required>
            </div>

            <div class="input-group">
                <label>İdeal Şarj Süresi (Dakika - %10-80)</label>
                <input type="number" name="charge" value="30" placeholder="Örn: 25" required>
            </div>

            {% for field, label in [
                ('pedal', 'Gaz Pedal Hassasiyeti'),
                ('regen', 'Rejenerasyon (Frenleme) Gücü'),
                ('comfort', 'Sürüş Konforu ve Süspansiyon'),
                ('multimedia', 'Ekran ve Yazılım Deneyimi'),
                ('seat', 'Koltuk ve Ergonomi'),
                ('material', 'İç Malzeme Kalitesi')
            ] %}
            <div class="input-group">
                <label>{{ label }}</label>
                <div class="slider-wrapper">
                    <input type="range" name="{{ field }}" min="1" max="10" value="5" oninput="this.nextElementSibling.innerText = this.value">
                    <div class="val-badge">5</div>
                </div>
            </div>
            {% endfor %}

            <button type="submit">En Uygun Aracı Analiz Et</button>
        </form>

        {% if result %}
            {% if result.status == "success" %}
                <div class="result">
                    <h2 style="margin-top:0; color:#007bff;">🎯 Önerimiz: {{ result.car.name }}</h2>
                    <div class="spec-row">
                        <span class="spec-label">Anahtar Teslim Fiyat:</span>
                        <span class="spec-val">{{ "{:,}".format(result.car.price).replace(",", ".") }} TL</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Fabrika Menzili:</span>
                        <span class="spec-val">{{ result.car.range_km }} km</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Şarj Süresi (%10-80):</span>
                        <span class="spec-val">{{ result.car.charge_time }} dakika</span>
                    </div>
                    <div class="spec-row">
                        <span class="spec-label">Konfor Puanı:</span>
                        <span class="spec-val">{{ result.car.comfort }}/10</span>
                    </div>
                </div>
            {% else %}
                <div class="error">
                    <h3>Uyumsuzluk!</h3>
                    <p>{{ result.msg }}</p>
                </div>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
