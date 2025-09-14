from flask import Flask, render_template_string, request, redirect, url_for, make_response
import os

app = Flask(__name__)

ROLL_NUMBERS = [f"24AI{str(i).zfill(3)}" for i in range(1, 59)]
PRESENT_FILE = "Present.txt"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Attendance Verification</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        select, button { font-size: 18px; padding: 10px; margin: 10px; }
    </style>
</head>
<body>
    <h1>Attendance Verification</h1>
    {% if marked %}
        <p style="color: green; font-size: 20px;">Attendance marked for {{ roll }} ✅</p>
        <p style="color: red; font-size: 18px;">This session is now closed.</p>
    {% else %}
        <form method="POST" action="/verify">
            <label for="roll">Select Roll Number:</label><br>
            <select name="roll" id="roll" required>
                {% for roll in rolls %}
                    <option value="{{ roll }}">{{ roll }}</option>
                {% endfor %}
            </select><br><br>
            <button type="submit">Verify with Fingerprint</button>
        </form>
        {% if message %}
            <p style="color: green; font-size: 20px;">{{ message }}</p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

def mark_present(roll):
    if not os.path.exists(PRESENT_FILE):
        open(PRESENT_FILE, "w").close()

    with open(PRESENT_FILE, "r") as f:
        lines = {line.strip() for line in f if line.strip()}

    if roll not in lines:
        with open(PRESENT_FILE, "a") as f:
            f.write(roll + "\n")

@app.route("/", methods=["GET"])
def home():
    marked = request.cookies.get("attendance_done", "no") == "yes"
    roll = request.cookies.get("roll", None)
    return render_template_string(HTML_TEMPLATE, rolls=ROLL_NUMBERS, message=None, marked=marked, roll=roll)

@app.route("/verify", methods=["POST"])
def verify():
    roll = request.form.get("roll")
    if roll:
        mark_present(roll)
        resp = make_response(render_template_string(HTML_TEMPLATE, rolls=ROLL_NUMBERS,
                                                    message=None, marked=True, roll=roll))
        # Set cookie so this phone session is locked
        resp.set_cookie("attendance_done", "yes", max_age=300)  # expires in 5 min
        resp.set_cookie("roll", roll, max_age=300)
        return resp
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
