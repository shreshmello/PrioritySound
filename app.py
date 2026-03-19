# PrioritySound Web Application
# A Flask-based web app for real-time sound detection and emergency alerting
# Uses machine learning to classify sounds and notify users based on customizable priorities

from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils import simulate_alert
import json
from datetime import datetime
from classifier import SoundClassifier
from detection_buffer import DetectionBuffer
import threading

app = Flask(__name__)
app.secret_key = "prioritysound_secret"
buffer = DetectionBuffer(size=5, required_matches=3)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prioritysound.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

classifier = None
classifier_lock = threading.Lock()

detection_thread = None
stop_event = threading.Event()
prediction_lock = threading.Lock()
user_context_lock = threading.Lock()
threshold = 0.5

alerts_feed = []

latest_prediction = {
    "label": None,
    "score": 0,
    "raw_label": None,
    "results": [],
    "accepted": False,
    "timestamp": None
}

active_detection_context = {
    "user_id": None,
    "preferences": {}
}

feedback_list = []

AVAILABLE_SOUNDS = [
    "baby crying",
    "doorbell ringing",
    "smoke alarm",
    "fire alarm",
    "police siren",
    "ambulance siren",
    "car horn"
]

MODES = {
    "Parent": {"baby crying": "high", "doorbell ringing": "medium"},
    "Home": {"doorbell ringing": "high", "smoke alarm": "emergency"},
    "Work": {"baby crying": "ignore", "doorbell ringing": "ignore"},
    "Night": {"doorbell ringing": "low", "smoke alarm": "emergency"}
}


def get_classifier():
    """Initialize and return the sound classifier singleton"""
    global classifier
    with classifier_lock:
        if classifier is None:
            classifier = SoundClassifier(
                labels_file="labels.csv",
                sample_rate=16000,
                duration=2
            )
    return classifier


def normalize_prediction(data):
    """Normalize prediction results to ensure consistent format"""
    results = data.get("results", []) or []

    top_label = data.get("label")
    top_score = float(data.get("score", 0) or 0)

    if results:
        parsed = []
        for item in results:
            if isinstance(item, dict):
                parsed.append({
                    "label": item.get("label"),
                    "score": float(item.get("score", 0) or 0)
                })
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                parsed.append({
                    "label": item[0],
                    "score": float(item[1] or 0)
                })

        if parsed:
            parsed.sort(key=lambda x: x["score"], reverse=True)
            if parsed[0]["label"]:
                top_label = parsed[0]["label"]
                top_score = parsed[0]["score"]
            results = parsed

    return {
        "label": top_label,
        "score": top_score,
        "raw_label": data.get("raw_label", top_label),
        "results": results,
        "accepted": bool(data.get("accepted", top_score >= 0.5))
    }


def detector_callback(data):
    global latest_prediction, alerts_feed, buffer, threshold
    """Process sound classification results and create alerts"""
    global latest_prediction, alerts_feed

    normalized = normalize_prediction(data)
    timestamp = datetime.now().strftime("%I:%M %p")

    with prediction_lock:
        latest_prediction = {
            **normalized,
            "timestamp": timestamp
        }

    if normalized.get("label"):
        sound = normalized["label"]
        score = normalized["score"]
        if score > threshold:
            confirmed_sound = sound
            avg_conf = score
            print(avg_conf)
        else:
            buffer.add(sound, score)
            result = buffer.confirmed(threshold)
            if not result:
                return
            confirmed_sound, avg_conf = result
            print(avg_conf)
        with user_context_lock:
            preferences = active_detection_context.get("preferences", {}) or {}

        priority = preferences.get(confirmed_sound, "low")
        if priority == "ignore":
            return

        alert = simulate_alert(confirmed_sound, priority, timestamp)
        alert["score"] = avg_conf

        if not alerts_feed or alerts_feed[0].get("sound") != confirmed_sound:
            alerts_feed.insert(0, alert)
            print('added to alerts!')
            if len(alerts_feed) > 20:
                alerts_feed.pop()


def detection_worker():
    """Background thread function for continuous sound classification"""
    clf = get_classifier()
    clf.classify_continuously(
        callback=detector_callback,
        stop_event=stop_event,
        min_confidence=0.5
    )


def start_background_detection(user_id):
    """Start background sound detection thread for user"""
    global detection_thread

    user = User.query.get(user_id)
    preferences = json.loads(user.preferences) if user and user.preferences else {}

    with user_context_lock:
        active_detection_context["user_id"] = user_id
        active_detection_context["preferences"] = preferences

    if detection_thread and detection_thread.is_alive():
        return

    stop_event.clear()
    detection_thread = threading.Thread(target=detection_worker, daemon=True)
    detection_thread.start()


def stop_background_detection():
    """Stop background sound detection"""
    stop_event.set()

# Authentication Routes
@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration"""
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(email=email).first():
            return "Email exists!"

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/start_dashboard")

        return "Invalid credentials!"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    stop_background_detection()
    return redirect("/login")

# Dashboard
@app.route("/")
def landing():
    return redirect("/login")
@app.route("/ar")
def ar_view():
    """Augmented reality view for sound visualization"""
    if "user_id" not in session:
        return redirect("/login")
    return render_template("ar.html")

@app.route("/start_dashboard")
def start_dashboard():
    """Loading screen before dashboard"""
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboardloading.html")


@app.route("/dashboard")
def dashboard():
    """Main dashboard with sound detection controls"""
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    preferences = json.loads(user.preferences) if user.preferences else {}

    return render_template(
        "dashboard.html",
        email=user.email,
        preferences=preferences,
        alerts=alerts_feed,
        mode=user.mode or "Custom"
    )

# Preferences
@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    """Manage user sound priority preferences"""
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        prefs = {}
        for sound in AVAILABLE_SOUNDS:
            level = request.form.get(sound)
            if level and level != "ignore":
                prefs[sound] = level

        user.preferences = json.dumps(prefs)
        db.session.commit()
        return redirect("/dashboard")

    return render_template("preferences.html", sounds=AVAILABLE_SOUNDS)

# Modes
@app.route("/modes", methods=["GET", "POST"])
def modes():
    """Select predefined priority modes (Parent, Home, Work, Night)"""
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        selected_mode = request.form.get("mode")
        if selected_mode in MODES:
            user.mode = selected_mode
            user.preferences = json.dumps(MODES[selected_mode])
            db.session.commit()
        return redirect("/dashboard")

    return render_template("mode.html", modes=MODES.keys(), current_mode=user.mode or "Custom")

# History/analytics of user
@app.route("/history")
def history():
    """View past sound detection alerts"""
    if "user_id" not in session:
        return redirect("/login")

    return render_template("history.html", alerts=alerts_feed)
# Sound Detection API Routes
@app.route("/start_detection", methods=["POST"])
def start_detection():
    """Start real-time sound detection in background thread"""
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    start_background_detection(session["user_id"])
    return jsonify({"status": "started"})

@app.route('/set_bg_threshold', methods = ["POST"])
def set_threshold():
    global threshold
    if threshold == 0.5:
        threshold = 0.3
    elif threshold == 0.3:
        threshold = 0.5
    else:
        threshold  = 0.5
    return jsonify({"threshold": threshold})
@app.route("/stop_detection", methods=["POST"])
def stop_detection():
    """Stop ongoing sound detection"""
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    stop_background_detection()
    return jsonify({"status": "stopped"})


@app.route("/latest_prediction", methods=["GET"])
def get_latest_prediction():
    """Get the most recent sound classification result"""
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    with prediction_lock:
        return jsonify(latest_prediction)


@app.route("/alerts_feed", methods=["GET"])
def get_alerts_feed():
    """Get list of recent alerts for real-time updates"""
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    return jsonify({"alerts": alerts_feed})

@app.route("/clear_history", methods=["POST"])
def clear_history():
    """Clear all stored alerts from memory"""
    global alerts_feed
    alerts_feed.clear()
    return redirect(url_for("history"))

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    """Handle user feedback submission and display form"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        # Store feedback
        feedback_entry = {
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        feedback_list.append(feedback_entry)
        print(f"Feedback received: {feedback_entry}")
        return render_template("feedback.html", submitted=True)
    return render_template("feedback.html", submitted=False)

@app.route("/admin/feedback")
def view_feedback():
    """Admin view to see all submitted feedback"""
    return render_template("admin_feedback.html", feedback_list=feedback_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True, threaded=True)
