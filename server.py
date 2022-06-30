import json
from re import L
from flask import Flask

app = Flask(__name__)

@app.route("/dados", methods=['GET'])
def index():
    file_csv = open('uber_prices_data.csv', 'r', newline='', encoding='utf-8')
    file_csv_read = file_csv.read()
    list = file_csv_read.replace("\r", '').split("\n")

    list_json = []

    for i in list:
        list_json.append(i.split(","))

    list_json.pop(-1)

    json_data = json.dumps(list_json)

    return json_data

if __name__ == "__main__":
    app.run(port=7500, host='0.0.0.0', debug=True, threaded=True)