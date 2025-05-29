from flask import Flask, request, render_template, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "converted"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["csvfile"]
        if file.filename.endswith(".csv"):
            filename = secure_filename(file.filename)
            csv_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(csv_path)

            # Convert to Excel
            df = pd.read_csv(csv_path)
            excel_filename = filename.replace(".csv", ".xlsx")
            excel_path = os.path.join(OUTPUT_FOLDER, excel_filename)
            df.to_excel(excel_path, index=False)

            return send_file(excel_path, as_attachment=True)
        else:
            return "Please upload a .csv file only.", 400

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)