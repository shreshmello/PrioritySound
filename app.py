from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils import simulate_alert
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "prioritysound_secret"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prioritysound.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Available sounds & modes
AVAILABLE_SOUNDS = ["baby crying", "doorbell ringing", "smoke alarm", "fire alarm",
                    "police siren", "ambulance siren", "car horn"]

MODES = {
    "Parent": {"baby crying": "high", "doorbell ringing": "medium"},
    "Home": {"doorbell ringing": "high", "smoke alarm": "emergency"},
    "Work": {"baby crying": "ignore", "doorbell ringing": "ignore"},
    "Night": {"doorbell ringing": "low", "smoke alarm": "emergency"}
}

# ----------------------
# AUTH ROUTES
# ----------------------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        if User.query.filter_by(email=email).first():
            return "Email exists!"
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            session["user_id"] = user.id
            return redirect("/start_dashboard")
        return "Invalid credentials!"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ----------------------
# DASHBOARD
# ----------------------
alerts_feed = []  # live feed

@app.route("/start_dashboard")
def start_dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboardloading.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    preferences = json.loads(user.preferences) if user.preferences else {}
    return render_template("dashboard.html", email=user.email, preferences=preferences, alerts=alerts_feed, mode=user.mode)

# ----------------------
# PREFERENCES
# ----------------------
@app.route("/preferences", methods=["GET","POST"])
def preferences():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    if request.method=="POST":
        prefs = {}
        for sound in AVAILABLE_SOUNDS:
            level = request.form.get(sound)
            if level and level!="ignore":
                prefs[sound] = level
        user.preferences = json.dumps(prefs)
        db.session.commit()
        return redirect("/dashboard")
    return render_template("preferences.html", sounds=AVAILABLE_SOUNDS)

# ----------------------
# MODES
# ----------------------
@app.route("/modes", methods=["GET","POST"])
def modes():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    if request.method=="POST":
        selected_mode = request.form.get("mode")
        if selected_mode in MODES:
            user.mode = selected_mode
            user.preferences = json.dumps(MODES[selected_mode])
            db.session.commit()
        return redirect("/dashboard")
    return render_template("modes.html", modes=MODES.keys(), current_mode=user.mode)

# ----------------------
# HISTORY / ANALYTICS
# ----------------------
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("history.html", alerts=alerts_feed)

# ----------------------
# SIMULATE ALERT (TSA DEMO)
# ----------------------
@app.route("/simulate_alert", methods=["POST"])
def simulate_alert_route():
    sound = request.form.get("sound")
    priority = request.form.get("priority")
    timestamp = datetime.now().strftime("%I:%M %p")
    alert = simulate_alert(sound, priority, timestamp)
    alerts_feed.insert(0, alert)  # add to top of feed
    if len(alerts_feed)>20:
        alerts_feed.pop()
    return jsonify({"status":"ok", "alert":alert})

# ----------------------
# RUN SERVER
# ----------------------
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
