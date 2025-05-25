from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Varsayılan varlıklar
assets = {
    "XAUUSD": {"pip_size": 0.01, "pip_value": 1.0},
    "EURUSD": {"pip_size": 0.0001, "pip_value": 10.0},
    "BTCUSD": {"pip_size": 1.0, "pip_value": 0.01},
    "AUDUSD": {"pip_size": 0.0001, "pip_value": 10.0},  # Avustralya Doları / ABD Doları
    "XAGUSD": {"pip_size": 0.01, "pip_value": 50.0},   # Gümüş / ABD Doları
    "USDCHF": {"pip_size": 0.0001, "pip_value": 10.0}, # ABD Doları / İsviçre Frangı
    "GBPUSD": {"pip_size": 0.0001, "pip_value": 10.0}, # İngiliz Sterlini / ABD Doları
    "ETHUSD": {"pip_size": 0.01, "pip_value": 0.1},    # Ethereum / ABD Doları
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            # Kullanıcıdan gelen verileri al
            balance = float(request.form["balance"])
            calculation_type = request.form["calculation_type"]
            sl_price = float(request.form["sl_price"])
            entry_price = float(request.form["entry_price"])
            tp_price = float(request.form.get("tp_price", 0))  # TP Fiyatı kontrolü
            asset = request.form["asset"]

            # Varlık bilgilerini al
            pip_size = assets[asset]["pip_size"]
            pip_value = assets[asset]["pip_value"]

            # Hesaplamalar
            if calculation_type == "Risk Yüzdesi":
                risk_percent = float(request.form["risk_percent"])
                risk_amount = balance * (risk_percent / 100)
            elif calculation_type == "Zarar Tutarı":
                risk_amount = float(request.form["risk_amount"])
            else:
                result = "Zarar türü seçilmedi!"
                return render_template("index.html", result=result)

            pip_distance = abs(entry_price - sl_price) / pip_size
            lot_size = risk_amount / (pip_distance * pip_value)
            tp_pip = abs(tp_price - entry_price) / pip_size
            tp_profit = tp_pip * pip_value * lot_size
            sl_loss = risk_amount

            # Modal içeriği
            result = f"""
                <h2>İşlem Özeti</h2>
                <p><strong>Varlık:</strong> {asset}</p>
                <p><strong>Giriş Fiyatı:</strong> {entry_price}</p>
                <p><strong>SL Fiyatı:</strong> {sl_price}</p>
                <p><strong>TP Fiyatı:</strong> {tp_price}</p>
                <p><strong>Lot Miktarı:</strong> {lot_size:.2f}</p>
                <p><strong>TP Karı:</strong> {tp_profit:.2f} USD</p>
                <p><strong>SL Zararı:</strong> {sl_loss:.2f} USD</p>
            """
        except ValueError:
            result = "Lütfen tüm alanları doğru doldurun!"
    return render_template("index.html", result=result, assets=assets.keys())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)