import sqlite3
import os
from io import BytesIO

from flask import Flask, render_template, request, redirect, session, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas

from sentence_transformers import SentenceTransformer, util

from resume_parser import extract_text
from job_recommender import recommend_jobs
from interview_generator import generate_questions
from ats_checker import get_missing_keywords, ai_resume_suggestions

# ================= APP ================= #
app = Flask(__name__)
app.secret_key = "ai_resume_analyzer_secret_key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ================= AI MODEL ================= #
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_ats_score(resume_text, job_description):
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    job_emb = model.encode(job_description, convert_to_tensor=True)

    score = util.cos_sim(resume_emb, job_emb).item()
    return round(score * 100, 2)

# ================= DB ================= #
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= HOME ================= #
@app.route("/")
def home():
    return render_template("home.html")

# ================= REGISTER ================= #
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            return render_template("register.html", error="User already exists")

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, hashed_pw)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ================= LOGIN ================= #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        is_admin = request.form.get("is_admin")

        if is_admin:
            if username == "admin" and password == "admin123":
                session["username"] = "admin"
                session["role"] = "admin"
                return redirect("/admin")
            return render_template("login.html", error="Invalid admin credentials")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT username, password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["username"] = user[0]
            session["role"] = "user"
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ================= LOGOUT ================= #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= DASHBOARD ================= #
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session["username"])

# ================= PROFILE ================= #
@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect("/login")
    return render_template("profile.html", username=session["username"])

# ================= RESUME ANALYSIS ================= #
@app.route("/resume_analysis", methods=["POST"])
def resume_analysis():

    file = request.files["resume"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    resume_text = extract_text(path)

    jobs = recommend_jobs(resume_text)

    return render_template(
        "result.html",
        result_type="resume",
        text=resume_text,
        jobs=jobs
    )
# ================= ATS ANALYSIS ================= #
@app.route("/ats_analysis", methods=["POST"])
def ats_analysis():

    if "username" not in session:
        return redirect("/login")

    file = request.files["resume"]
    job_description = request.form["job_description"]

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    resume_text = extract_text(path)

    score = calculate_ats_score(resume_text, job_description)

    missing = get_missing_keywords(
        resume_text,
        job_description
    )

    suggestions = ai_resume_suggestions(
        score,
        missing
    )

    improved_resume = f"""
ATS SCORE: {score}%

Missing Keywords:
{', '.join(missing)}

Suggestions:
{suggestions}
"""

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resume_history
        (username, resume_name, ats_score)
        VALUES (?, ?, ?)
    """, (
        session["username"],
        file.filename,
        score
    ))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        result_type="ats",
        score=score,
        missing=missing,
        suggestions=suggestions,
        improved_resume=improved_resume
    )
# ================= ATS CHECKER ================= #
@app.route("/ats_checker")
def ats_checker():
    if "username" not in session:
        return redirect("/login")
    return render_template("ats_checker.html")


@app.route("/analyzer")
def analyzer():
    if "username" not in session:
        return redirect("/login")
    return render_template("analyzer.html")


@app.route("/interview")
def interview():
    if "username" not in session:
        return redirect("/login")
    return render_template("interview.html")


@app.route("/settings/password")
def settings_password():
    if "username" not in session:
        return redirect("/login")
    return render_template("settings_password.html")
# ================= INTERVIEW ================= #
@app.route("/generate_interview", methods=["POST"])
def generate_interview():
    if "username" not in session:
        return redirect("/login")

    role = request.form["role"]
    company = request.form["company"]
    jd = request.form["job_description"]

    questions = generate_questions(role, company, jd)

    return render_template("result.html",
                           result_type="interview",
                           questions=questions)

# ================= HISTORY ================= #
@app.route("/history")
def history():
    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT resume_name, ats_score, upload_date
        FROM resume_history
        WHERE username=?
        ORDER BY upload_date DESC
    """, (session["username"],))

    history = cursor.fetchall()
    conn.close()

    return render_template("history.html", history=history)

# ================= DOWNLOAD REPORT ================= #
@app.route("/download_report")
def download_report():
    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT resume_name, ats_score
        FROM resume_history
        WHERE username=?
        ORDER BY id DESC
        LIMIT 1
    """, (session["username"],))

    data = cursor.fetchone()
    conn.close()

    if not data:
        return "No report found"

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 800, "AI Resume Analyzer Report")
    pdf.drawString(100, 750, f"User: {session['username']}")
    pdf.drawString(100, 720, f"Resume: {data[0]}")
    pdf.drawString(100, 690, f"ATS Score: {data[1]}")

    pdf.save()
    buffer.seek(0)

    return send_file(buffer,
                     as_attachment=True,
                     download_name="report.pdf",
                     mimetype="application/pdf")

# ================= CHANGE PASSWORD ================= #
@app.route("/change_password", methods=["POST"])
def change_password():
    if "username" not in session:
        return redirect("/login")

    old = request.form["old_password"]
    new = request.form["new_password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?",
                   (session["username"],))
    user = cursor.fetchone()

    if not user or not check_password_hash(user[0], old):
        return render_template("settings_password.html",
                               error="Old password incorrect")

    new_hash = generate_password_hash(new)

    cursor.execute("UPDATE users SET password=? WHERE username=?",
                   (new_hash, session["username"]))

    conn.commit()
    conn.close()

    return render_template("settings_password.html",
                           success="Password updated successfully")
# ================= DARK MODE ================= #
@app.route('/toggle_dark')
def toggle_dark():
    session['dark'] = not session.get('dark', False)
    return redirect(request.referrer or "/dashboard")
# ================= ADMIN ================= #
@app.route("/admin")
def admin_dashboard():

    if session.get("role") != "admin":
        return render_template("access_denied.html"), 403

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM resume_history")
    total_reports = cursor.fetchone()[0]

    cursor.execute("SELECT ats_score FROM resume_history")
    scores = cursor.fetchall()

    ats_scores = [s[0] for s in scores if s[0] is not None]

    cursor.execute("""
        SELECT id, username, resume_name, ats_score, upload_date
        FROM resume_history
        ORDER BY id DESC
    """)
    reports = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        users=users,
        total_users=total_users,
        total_reports=total_reports,
        reports=reports,
        ats_scores=ats_scores
    )
# ================= JOB RECOMMENDED ================= #
def recommend_jobs(text):

    text = text.lower()

    jobs = []

    if "python" in text:
        jobs.append("Python Developer")

    if "java" in text:
        jobs.append("Java Developer")

    if "sql" in text:
        jobs.append("Database Developer")

    if "machine learning" in text:
        jobs.append("Machine Learning Engineer")

    if "data science" in text:
        jobs.append("Data Scientist")

    if "html" in text or "css" in text or "javascript" in text:
        jobs.append("Frontend Developer")

    if "flask" in text or "django" in text:
        jobs.append("Backend Developer")

    if "react" in text:
        jobs.append("React Developer")

    if "aws" in text:
        jobs.append("Cloud Engineer")

    if not jobs:
        jobs.append("Software Engineer")

    return jobs
# ================= RUN ================= #
if __name__ == "__main__":
    app.run(debug=True)