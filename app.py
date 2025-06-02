from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/',)
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if not file:
        return 'No file uploaded.', 400

    # CSV to Excel
    df = pd.read_csv(file)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)

    return send_file(output, download_name='converted.xlsx', as_attachment=True)

@app.route('/convert_excel', methods=['POST'])
def convert_excel():
    file = request.files['file']
    if not file:
        return 'No file uploaded.', 400

    # Excel to CSV
    df = pd.read_excel(file)

    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, download_name='converted.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
