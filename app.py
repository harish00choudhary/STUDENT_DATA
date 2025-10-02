from flask import Flask, render_template, request, redirect, url_for, flash
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)
app.secret_key = "student_portal_secret"  # for flashing messages

# Google Sheets Setup
USE_GOOGLE_SHEETS = True  # set False if using local Excel



def load_data():
    if USE_GOOGLE_SHEETS:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json"), scope)
        client = gspread.authorize(creds)

        sheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        sheet = client.open_by_key(sheet_id).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
    else:
        # fallback: local Excel
        df = pd.read_excel("students.xlsx")
    return df


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        enrollment_number = request.form.get("enrollment")
        if not enrollment_number:
            flash("⚠ Please enter an enrollment number")
            return redirect(url_for("index"))

        df = load_data()
        student = df.loc[df["Enrollment Number"].astype(str) == enrollment_number]

        if student.empty:
            flash("❌ No student found with this enrollment number")
            return redirect(url_for("index"))

        student_data = student.iloc[0].to_dict()
        return render_template("student_info.html", student=student_data)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
