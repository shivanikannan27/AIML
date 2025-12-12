from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Rock Paper Scissors</title>
  <style>
    body{font-family:sans-serif;display:flex;flex-direction:column;align-items:center;gap:12px;padding:40px}
    button{padding:10px 18px;font-size:16px;border-radius:8px;cursor:pointer}
    #result{margin-top:12px;font-weight:600}
  </style>
</head>
<body>
  <h1>Rock · Paper · Scissors</h1>
  <div>
    <button onclick="play('rock')">🪨 Rock</button>
    <button onclick="play('paper')">📄 Paper</button>
    <button onclick="play('scissors')">✂️ Scissors</button>
  </div>
  <div id="result"></div>

  <script>
    async function play(choice){
      const res = await fetch('/play', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({player: choice})
      });
      const data = await res.json();
      document.getElementById('result').innerText =
        `You: ${data.player} — CPU: ${data.cpu} — Result: ${data.result}`;
    }
  </script>
</body>
</html>
"""

# game logic
WIN_MAP = {
    'rock': 'scissors',
    'scissors': 'paper',
    'paper': 'rock'
}

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/play", methods=["POST"])
def play():
    data = request.get_json() or {}
    player = (data.get("player") or "").lower()
    if player not in WIN_MAP:
        return jsonify({"error": "invalid choice"}), 400

    cpu = random.choice(list(WIN_MAP.keys()))
    if player == cpu:
        result = "draw"
    elif WIN_MAP[player] == cpu:
        result = "Congrats you won the game!"
    else:
        result = "Oops you Lose the Game"

    return jsonify({"player": player, "cpu": cpu, "result": result})

if __name__ == "__main__":
    app.run(debug=True)
