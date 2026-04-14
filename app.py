# PrioritySound Web Application (CLEAN VERSION)

from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils import simulate_alert
from datetime import datetime
from classifier import SoundClassifier
from detection_buffer import DetectionBuffer
from emergency_detector import EmergencySoundDetector
import threading
import json
import random

app = Flask(__name__)
app.secret_key = "prioritysound_secret"

# DB setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prioritysound.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- STATE ----------------
classifier = None
classifier_lock = threading.Lock()

detection_thread = None
stop_event = threading.Event()

prediction_lock = threading.Lock()
user_context_lock = threading.Lock()

buffer = DetectionBuffer(size=5, required_matches=3)
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

# ---------------- CLASSIFIER ----------------
def get_classifier():
    global classifier
    with classifier_lock:
        if classifier is None:
            classifier = SoundClassifier(
                labels_file="labels.csv",
                sample_rate=16000,
                duration=2
            )
    return classifier


# ---------------- NORMALIZE ----------------
def normalize_prediction(data):
    results = data.get("results", []) or []

    top_label = data.get("label")
    top_score = float(data.get("score", 0) or 0)

    parsed = []
    for item in results:
        if isinstance(item, dict):
            parsed.append({
                "label": item.get("label"),
                "score": float(item.get("score", 0) or 0)
            })

    if parsed:
        parsed.sort(key=lambda x: x["score"], reverse=True)
        top_label = parsed[0]["label"]
        top_score = parsed[0]["score"]
        results = parsed

    return {
        "label": top_label,
        "score": top_score,
        "raw_label": data.get("raw_label", top_label),
        "results": results,
        "accepted": top_score >= threshold
    }


# ---------------- DETECTION CALLBACK ----------------
def detector_callback(data):
    global latest_prediction, alerts_feed
    try:
        normalized = normalize_prediction(data)
        timestamp = datetime.now().strftime("%I:%M %p")

        with prediction_lock:
            latest_prediction.update(normalized)
            latest_prediction["timestamp"] = timestamp

        if not normalized["label"]:
            print("[callback] no label, returning")
            return

        sound = normalized["label"]
        score = normalized["score"]
        print(f"[callback] sound={sound}, score={score:.2f}, threshold={threshold}")

        if score > threshold:
            confirmed_sound = sound
            avg_conf = score
            print(f"[callback] fast path: {confirmed_sound} at {avg_conf:.2f}")
        else:
            buffer.add(sound, score)
            result = buffer.confirmed(threshold)
            print(f"[callback] buffer result: {result}")
            if not result:
                return
            confirmed_sound, avg_conf = result
            buffer.clear()

        with user_context_lock:
            prefs = dict(active_detection_context["preferences"])
        print(f"[callback] prefs={prefs}")

        detector = EmergencySoundDetector(prefs, active_threshold=threshold)
        priority = detector.get_alert_level(confirmed_sound, avg_conf)
        print(f"[callback] priority={priority}")

        if priority == "ignore":
            print("[callback] ignored by detector")
            return

        alert = simulate_alert(confirmed_sound, priority, timestamp)
        alert["score"] = avg_conf

        last_alert = alerts_feed[0] if alerts_feed else None
        is_duplicate = (
            last_alert and
            last_alert["sound"] == confirmed_sound and
            last_alert["time"] == timestamp
        )
        print(f"[callback] is_duplicate={is_duplicate}")

        if not is_duplicate:
            alerts_feed.insert(0, alert)
            if len(alerts_feed) > 20:
                alerts_feed.pop()
            print(f"[callback] alert inserted: {alert}")

    except Exception as e:
        print(f"[detector_callback ERROR] {e}")
    

# ---------------- BACKGROUND THREAD ----------------
def detection_worker():
    clf = get_classifier()
    clf.classify_continuously(
        callback=detector_callback,
        stop_event=stop_event,
        min_confidence=0.5
    )


def start_background_detection(user_id):
    global detection_thread

    user = User.query.get(user_id)
    if user and user.preferences:
        preferences = json.loads(user.preferences)
    else:
        preferences = {}
    with user_context_lock:
        active_detection_context["user_id"] = user_id
        active_detection_context["preferences"] = preferences

    if detection_thread and detection_thread.is_alive():
        return

    stop_event.clear()
    detection_thread = threading.Thread(target=detection_worker, daemon=True)
    detection_thread.start()


def stop_background_detection():
    stop_event.set()


# ---------------- AUTH ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(email=email).first():
            return "Email exists!"

        db.session.add(User(email=email, password=password))
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            return redirect("/dashboard")

        return "Invalid credentials!"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    stop_background_detection()
    return redirect("/login")


# ---------------- PAGES ----------------
@app.route("/")
def landing():
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    prefs = json.loads(user.preferences) if user.preferences else {}

    return render_template(
        "dashboard.html",
        email=user.email,
        preferences=prefs,
        alerts=alerts_feed,
        mode= session.get("mode", user.mode or "Custom")
    )
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == 'POST':
        feedback_list.append({
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "message": request.form.get("message", ""),
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "user_id": session["user_id"]
        })
        return render_template('feedback.html', submitted=True)
    
    return render_template('feedback.html', submitted=False)

@app.route('/history')
def history():
    if "user_id" not in session:
        return redirect("/login")
    return render_template('history.html', alerts=alerts_feed)

@app.route('/clear_history', methods=["POST"])
def clear_history():
    if "user_id" not in session:
        return redirect("/login")
    global alerts_feed
    alerts_feed = []
    return redirect("/history")

@app.route('/modes', methods = ['GET', 'POST'])
def modes():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == 'POST':
        selected_mode = request.form.get("mode")
        if selected_mode:
            session['mode'] = selected_mode
            user = User.query.get(session["user_id"])
            user.preferences = json.dumps(MODES.get(selected_mode, {}))
            db.session.commit()
        return redirect('/dashboard')
    return render_template(
        'mode.html',
        modes = MODES,
        current_mode = session.get('mode', 'Custom'))

@app.route("/ar")
def ar_view():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("ar.html")


# ---------------- AR DATA (FIXED) ----------------
@app.route("/direction_data")
def direction_data():

    label = random.choice([
        "smoke alarm",
        "doorbell ringing",
        "car horn",
        "baby crying"
    ])

    priority_map = {
        "smoke alarm": "emergency",
        "doorbell ringing": "medium",
        "car horn": "high",
        "baby crying": "high"
    }

    angle = random.randint(0, 360)

    if 60 <= angle <= 120:
        direction = "right"
    elif 240 <= angle <= 300:
        direction = "left"
    else:
        direction = "center"

    return jsonify({
        "label": label,
        "priority": priority_map[label],
        "angle": angle,
        "direction": direction
    })


# ---------------- API ----------------
@app.route("/start_detection", methods=["POST"])
def start_detection():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    start_background_detection(session["user_id"])
    return jsonify({"status": "started"})


@app.route("/stop_detection", methods=["POST"])
def stop_detection():
    stop_background_detection()
    return jsonify({"status": "stopped"})


@app.route("/latest_prediction")
def latest():
    return jsonify(latest_prediction)


@app.route("/alerts_feed")
def alerts():
    return jsonify({"alerts": alerts_feed})


@app.route("/set_bg_threshold", methods=["POST"])
def set_threshold():
    global threshold
    threshold = 0.3 if threshold == 0.5 else 0.5
    print(f"[bg-noise] threshold set to {threshold}")
    return jsonify({"threshold": threshold})


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True, threaded=True)
