from flask import Flask, request, jsonify, send_from_directory
from string_calculator import StringCalculator
import os

app = Flask(__name__, static_folder="../frontend/dist", static_url_path="")
calc = StringCalculator()

@app.route("/api/add", methods=["POST"])
def api_add():
    try:
        data = request.get_json(force=True)
        input_str = data.get("input", "")
        result = calc.add(input_str)
        return jsonify({"ok": True, "result": result, "calledCount": calc.get_called_count()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route("/api/reset", methods=["POST"])
def api_reset():
    calc.reset_called_count()
    return jsonify({"ok": True, "calledCount": calc.get_called_count()})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
