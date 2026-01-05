import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)
DB_PATH = "cars.db"


# ---------- DB ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            price INTEGER,
            battery INTEGER,
            range_km INTEGER,
            charge_time INTEGER,
            multimedia INTEGER,
            seat_comfort INTEGER,
            regen INTEGER,
            interior_quality INTEGER
        )
        """)

    c.execute("SELECT COUNT(*) FROM cars")
    if c.fetchone()[0] == 0:
        cars = [
            # TESLA
            ("Tesla", "Model 3 SR", 1600000, 60, 510, 25, 9, 8, 9, 8),
            ("Tesla", "Model 3 LR", 1850000, 75, 602, 27, 9, 8, 9, 8),
            ("Tesla", "Model Y SR", 1650000, 60, 455, 27, 9, 8, 9, 8),
            ("Tesla", "Model Y LR", 1900000, 75, 533, 30, 9, 8, 9, 8),

            # TOGG
            ("Togg", "T10X V1", 1500000, 52, 314, 28, 7, 8, 8, 7),
            ("Togg", "T10X V2", 1800000, 88, 523, 32, 7, 8, 8, 7),

            # BMW
            ("BMW", "iX1", 1750000, 64, 440, 29, 8, 9, 7, 9),
            ("BMW", "i4 eDrive40", 2500000, 84, 590, 31, 9, 9, 8, 9),
            ("BMW", "iX", 3500000, 111, 630, 35, 9, 9, 8, 10),

            # MERCEDES
            ("Mercedes", "EQA 250", 1800000, 66, 426, 30, 9, 9, 7, 9),
            ("Mercedes", "EQB 250", 1900000, 66, 423, 30, 9, 9, 7, 9),
            ("Mercedes", "EQE", 3200000, 90, 639, 32, 10, 9, 8, 10),
            ("Mercedes", "EQS", 4500000, 108, 770, 36, 10, 10, 8, 10),

            # HYUNDAI
            ("Hyundai", "Kona Electric", 1400000, 64, 484, 30, 7, 7, 6, 7),
            ("Hyundai", "Ioniq 5", 1650000, 72, 507, 28, 8, 8, 7, 8),
            ("Hyundai", "Ioniq 6", 1750000, 77, 614, 28, 8, 8, 7, 8),

            # KIA
            ("Kia", "Niro EV", 1450000, 64, 460, 30, 7, 7, 6, 7),
            ("Kia", "EV6", 1850000, 77, 528, 28, 8, 8, 7, 8),

            # VOLKSWAGEN
            ("Volkswagen", "ID.3", 1550000, 58, 426, 29, 7, 7, 6, 7),
            ("Volkswagen", "ID.4", 1700000, 77, 520, 31, 7, 8, 6, 8),
            ("Volkswagen", "ID. Buzz", 2300000, 77, 423, 32, 8, 8, 6, 8),

            # AUDI
            ("Audi", "Q4 e-tron", 2000000, 77, 520, 31, 9, 9, 7, 9),
            ("Audi", "e-tron GT", 4200000, 93, 488, 34, 10, 9, 8, 10),

            # PEUGEOT / OPEL
            ("Peugeot", "e-208", 1250000, 50, 400, 27, 6, 6, 5, 6),
            ("Opel", "Corsa-e", 1200000, 50, 395, 27, 6, 6, 5, 6),
            ("Opel", "Mokka-e", 1350000, 50, 403, 28, 6, 6, 5, 6),

            # RENAULT
            ("Renault", "Megane E-Tech", 1550000, 60, 470, 29, 7, 7, 6, 7),

            # MINI / FIAT
            ("Mini", "Cooper SE", 1500000, 32, 234, 22, 7, 6, 6, 7),
            ("Fiat", "500e", 1100000, 42, 320, 24, 6, 5, 5, 6)
        ]

        c.executemany("""
            INSERT INTO cars
            (brand, model, price, battery, range_km, charge_time,
             multimedia, seat_comfort, regen, interior_quality)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, cars)

    conn.commit()
    conn.close()


init_db()


# ---------- ROUTE ----------
@app.route("/", methods=["GET", "POST"])
def index():
    cars = []
    if request.method == "POST":
        max_price = int(request.form["price"])
        min_range = int(request.form["range"])

        conn = get_db()
        c = conn.cursor()
        c.execute("""
            SELECT * FROM cars
            WHERE price <= ?
            AND range_km >= ?
            ORDER BY
            (multimedia + seat_comfort + regen + interior_quality) DESC
            """, (max_price, min_range))
        cars = c.fetchall()
        conn.close()

    return render_template_string("""
        <h2>Araç Öneri Sistemi</h2>

        <form method="post">
            Max Fiyat (TL):
            <input type="number" name="price" value="1600000"><br><br>
            Min Menzil (km):
            <input type="number" name="range" value="500"><br><br>
            <button type="submit">Araç Öner</button>
        </form>

        <hr>

        {% for c in cars %}
        <b>{{ c.brand }} {{ c.model }}</b>
        <ul>
            <li>Fiyat: {{ c.price }} TL</li>
            <li>Batarya: {{ c.battery }} kWh</li>
            <li>Menzil: {{ c.range_km }} km</li>
            <li>Şarj süresi: {{ c.charge_time }} dk</li>
            <li>Multimedya: {{ c.multimedia }}/10</li>
            <li>Koltuk rahatlığı: {{ c.seat_comfort }}/10</li>
            <li>Rejenerasyon: {{ c.regen }}/10</li>
            <li>İç malzeme kalitesi: {{ c.interior_quality }}/10</li>
        </ul>
        <hr>
        {% endfor %}
        """, cars=cars)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
