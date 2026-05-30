from flask import Flask, render_template, request, redirect
import re

app = Flask(__name__)

# =========================
# GLOBAL STORAGE
# =========================

logs_data = []

# =========================
# DASHBOARD
# =========================

@app.route("/")
def dashboard():

    total_logs = 0
    high_risk = 0
    medium_risk = 0
    low_risk = 0

    for item in logs_data:

        total_logs += item["attempts"]

        if item["risk"] == "High":
            high_risk += 1

        elif item["risk"] == "Medium":
            medium_risk += 1

        else:
            low_risk += 1

    return render_template(

        "dashboard.html",

        data=logs_data,

        total_logs=total_logs,

        high_risk=high_risk,

        medium_risk=medium_risk,

        low_risk=low_risk
    )

# =========================
# UPLOAD LOG FILE
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    global logs_data

    file = request.files.get("logfile")

    if not file:

        return redirect("/")

    content = file.read().decode(
        "utf-8",
        errors="ignore"
    )

    # Extract IPs

    ips = re.findall(

        r'(?:\d{1,3}\.){3}\d{1,3}',

        content
    )

    ip_counts = {}

    for ip in ips:

        if ip in ip_counts:

            ip_counts[ip] += 1

        else:

            ip_counts[ip] = 1

    logs_data = []

    for ip, count in ip_counts.items():

        if count >= 10:

            risk = "High"

        elif count >= 5:

            risk = "Medium"

        else:

            risk = "Low"

        logs_data.append({

            "ip": ip,

            "attempts": count,

            "risk": risk
        })

    return redirect("/")

# =========================
# THREATS PAGE
# =========================

@app.route("/threats")
def threats():

    return render_template(

        "threats.html",

        data=logs_data
    )

# =========================
# ANALYTICS
# =========================

@app.route("/analytics")
def analytics():

    return render_template(

        "analytics.html"
    )

# =========================
# REPORTS
# =========================

@app.route("/reports")
def reports():

    return render_template(

        "reports.html"
    )

# =========================
# SETTINGS
# =========================

@app.route("/settings")
def settings():

    return render_template(

        "settings.html"
    )

# =========================
# INVESTIGATION
# =========================

@app.route("/investigate/<ip>")
def investigate(ip):

    found = None

    for item in logs_data:

        if item["ip"] == ip:

            found = item

            break

    return render_template(

        "investigate.html",

        threat=found
    )

# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(debug=True)