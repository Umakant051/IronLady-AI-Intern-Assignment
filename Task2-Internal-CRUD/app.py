from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "ironlady-demo-secret"  # ok for local demo (not a real secret)

DB_PATH = Path(__file__).with_name("enquiries.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            program TEXT,
            message TEXT,
            status TEXT NOT NULL DEFAULT 'New'
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()
    enquiries = conn.execute("SELECT * FROM enquiries ORDER BY id ASC").fetchall()
    conn.close()
    return render_template("index.html", enquiries=enquiries)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        program = request.form.get("program", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            flash("Name and Email are required.", "error")
            return render_template("form.html", mode="create", enquiry=None)

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO enquiries (name, email, phone, program, message, status) VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, phone, program, message, "New")
        )
        conn.commit()
        conn.close()

        flash("Enquiry created successfully!", "success")
        return redirect(url_for("index"))

    return render_template("form.html", mode="create", enquiry=None)


@app.route("/edit/<int:enquiry_id>", methods=["GET", "POST"])
def edit(enquiry_id):
    conn = get_db_connection()
    enquiry = conn.execute("SELECT * FROM enquiries WHERE id = ?", (enquiry_id,)).fetchone()

    if enquiry is None:
        conn.close()
        flash("Enquiry not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        program = request.form.get("program", "").strip()
        message = request.form.get("message", "").strip()
        status = request.form.get("status", "New").strip()

        if not name or not email:
            conn.close()
            flash("Name and Email are required.", "error")
            return render_template("form.html", mode="edit", enquiry=enquiry)

        conn.execute("""
            UPDATE enquiries
            SET name = ?, email = ?, phone = ?, program = ?, message = ?, status = ?
            WHERE id = ?
        """, (name, email, phone, program, message, status, enquiry_id))
        conn.commit()
        conn.close()

        flash("Enquiry updated successfully!", "success")
        return redirect(url_for("index"))

    conn.close()
    return render_template("form.html", mode="edit", enquiry=enquiry)


@app.route("/delete/<int:enquiry_id>", methods=["POST"])
def delete(enquiry_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM enquiries WHERE id = ?", (enquiry_id,))
    conn.commit()
    conn.close()

    flash("Enquiry deleted successfully!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
