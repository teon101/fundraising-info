from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_BASE = "https://api.crypto-fundraising.info"
API_TOKEN = "3VxHCLPfXkkKzRhJMWlO8kbP54JmxVt7kc7mvYQ3TRW4AS8SUrLdgul6ttH0z1ktpfSgJlFObSDVlKkqYharJpRKEVTlq5EImQb6YR9O5I6L3GAicV7Bp8oJ"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/rounds")
def get_rounds():
    lm = request.args.get("lm", "")
    offset = request.args.get("offset", "0")

    params = {"offset": offset}
    if lm:
        params["lm"] = lm

    try:
        res = requests.get(
            f"{API_BASE}/allrounds.php",
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            params=params,
            timeout=15
        )
        data = res.json()

        # Rounds are stored as numbered keys "0", "1", "2"...
        rounds = []
        i = 0
        while str(i) in data:
            round_item = data[str(i)]
            # Normalize field names (API uses "round_value(usd)" etc.)
            round_item["round_value"] = round_item.get("round_value(usd)", 0)
            round_item["round_valuation"] = round_item.get("round_valuation(usd)", 0)
            round_item["lead_investors"] = round_item.get("lead_investors_list", [])
            round_item["investors"] = round_item.get("investors_list", [])
            rounds.append(round_item)
            i += 1

        return jsonify({"ok": True, "results": rounds, "total": data.get("total_rounds", len(rounds))})

    except Exception as e:
        return jsonify({"ok": False, "description": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)