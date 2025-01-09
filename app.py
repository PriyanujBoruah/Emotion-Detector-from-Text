from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from transformers import pipeline, AutoTokenizer
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Get the secret key from the OS environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)


# --- Load Model ---
try:
    model_name = "SamLowe/roberta-base-go_emotions"
    classifier = pipeline(task="text-classification", model=model_name, top_k=None)  # No tokenizer here
    print("Emotion analysis model loaded successfully.")
except Exception as e:
    print(f"Error loading emotion analysis model: {e}")
    classifier = None
# --- End Load Model ---


login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    emotion_stats = db.Column(db.Text, nullable=False)  # Store as JSON string


@login_manager.user_loader  # Tells Flask-Login how to load users
def load_user(user_id):
    return User.query.get(int(user_id))

def predict_emotions(text):
    """Predicts emotions and returns probabilities."""
    if classifier is None:  # Only check classifier, not tokenizer
        return {"Error": "Emotion analysis model not loaded"}

    print(f"Predicting emotions for: '{text}'")
    try:
        model_outputs = classifier(text)  # Pipeline handles tokenization

        if isinstance(model_outputs, list) and len(model_outputs) > 0:
            emotion_scores = {result['label']: result['score'] for result in model_outputs[0]}
            return emotion_scores
        else:
            return {"Error": "No results from emotion model"}

    except Exception as e:
        print(f"Error during emotion prediction: {e}")
        return {"Error": f"An error occurred during emotion prediction: {str(e)}"}  # More informative error message

@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return None

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("register"))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please enter a username and password", "danger")
            return redirect(url_for("login"))

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))  # Redirect to index after login

        else:
            flash("Login unsuccessful. Please check username and password.", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        user_text = request.form["text"]
        emotion_predictions = predict_emotions(user_text)

        if "Error" not in emotion_predictions:
            json_string = json.dumps(emotion_predictions)
            analysis = Analysis(user_id=current_user.id, text=user_text, emotion_stats=json_string)
            db.session.add(analysis)
            db.session.commit()

        return render_template("index.html", text=user_text, emotion_predictions=emotion_predictions)

    analyses = Analysis.query.filter_by(user_id=current_user.id)
    return render_template("index.html", analyses=analyses)


@app.route("/api/analyses")
@login_required
def api_analyses():
    analyses = Analysis.query.filter_by(user_id=current_user.id)
    response = []

    for analysis in analyses:
        emotion_stats = json.loads(analysis.emotion_stats)
        response.append({
            "id": analysis.id,
            "text": analysis.text,
            "emotion_stats": emotion_stats
        })

    return jsonify(response)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)