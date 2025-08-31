from flask import Flask, render_template, request, redirect, url_for
import gspread
#from google.oauth2.service_account
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ---------------- Google Sheets Setup ----------------
# Define API scope
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Load credentials from JSON key file (downloaded from Google Cloud)
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Replace this with your Google Sheet ID
SPREADSHEET_ID = "1L842QiNYJB7mbnJlmz9gSpl0hhwFbD804TS_bNIr3e4"


#SPREADSHEET_ID = "https://docs.google.com/spreadsheets/d/1L842QiNYJB7mbnJlmz9gSpl0hhwFbD804TS_bNIr3e4/edit?usp=sharing"
#sheet = client.open_by_key(SPREADSHEET_ID).Hiring_Sheet
sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Sheet1")


# ---------------- Flask Routes ----------------
@app.route("/", methods=["GET"])
def page1():
    return render_template("page1.html")


@app.route("/submit", methods=["POST"])
def submit_form():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    branch = request.form.get("branch", "")
    year = request.form.get("year", "")

    # Save form data into Google Sheet
    sheet.append_row([name, email, phone, branch, year])
    print(f"✅ Saved to Google Sheet: {name}, {email}, {phone}, {branch}, {year}")

    # Redirect to Page 2
    return redirect(url_for("page2"))


@app.route("/page2", methods=["GET"])
def page2():
    return render_template("page2.html")


@app.route("/page2_submit", methods=["POST"])
def page2_submit():
    return redirect(url_for("page3"))


@app.route("/page3", methods=["GET"])
def page3():
    return render_template("page3.html")


# ---------------- Run Flask ----------------
if __name__ == "__main__":
    app.run(debug=True)
