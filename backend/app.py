from flask import Flask, request, jsonify, send_from_directory
from string_calculator import StringCalculator
import unittest
import io
import os

# Flask app, serving React build
app = Flask(__name__, static_folder="../frontend/dist", static_url_path="")

# ✅ Global calculator instance
calc = StringCalculator()


# ----------------------------
# Helper: prettify test names
# ----------------------------
def prettify_name(test_name: str) -> str:
    """
    Convert 'test_two_numbers_newline_delimited (module.Class.method)'
    -> 'Test two numbers newline delimited'
    """
    if "(" in test_name:
        raw_method = test_name.split("(")[0].strip()
    else:
        raw_method = test_name

    if raw_method.startswith("test_"):
        raw_method = raw_method[5:]

    return raw_method.replace("_", " ").capitalize()


# ----------------------------
# API: Add numbers
# ----------------------------
@app.route("/api/add", methods=["POST"])
def api_add():
    try:
        data = request.get_json(force=True)
        input_str = data.get("input", "")
        result = calc.add(input_str)
        return jsonify({
            "ok": True,
            "result": result,
            "calledCount": calc.get_called_count()
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


# ----------------------------
# API: Reset calculator state
# ----------------------------
@app.route("/api/reset", methods=["POST"])
def api_reset():
    global calc
    calc.__init__() # reset state
    return jsonify({"ok": True, "calledCount": calc.get_called_count()})


# ----------------------------
# API: Run tests
# ----------------------------
@app.route("/api/run-tests", methods=["POST"])
def api_run_tests():
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir=start_dir, pattern="test_*.py")

    # Flatten test names BEFORE running
    def iter_tests(suite):
        for t in suite:
            if isinstance(t, unittest.TestSuite):
                yield from iter_tests(t)
            else:
                yield t

    all_tests = [str(t) for t in iter_tests(suite)]

    # Run tests
    output_stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=output_stream, verbosity=2)
    result = runner.run(loader.discover(start_dir=start_dir, pattern="test_*.py"))
    raw_output = output_stream.getvalue()

    # Collect failed/error test names
    failed_or_errored = {}
    for test, err in result.errors:
        failed_or_errored[str(test)] = {"status": "error", "message": err}
    for test, err in result.failures:
        failed_or_errored[str(test)] = {"status": "failed", "message": err}

    # Build results
    results = []
    for i, test_name in enumerate(all_tests, start=1):
        pretty = prettify_name(test_name)
        if test_name in failed_or_errored:
            status = failed_or_errored[test_name]["status"]
            message = failed_or_errored[test_name]["message"]
        else:
            status = "passed"
            message = ""
        results.append({
            "id": i,
            "name": pretty,
            "status": status,
            "message": message
        })

    summary = {
        "total": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "passed": result.testsRun - len(result.failures) - len(result.errors),
    }

    return jsonify({
        "summary": summary,
        "results": results,
        "raw": raw_output
    })


# ----------------------------
# Serve React frontend
# ----------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
