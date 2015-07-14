#!/usr/bin/env python3
from flask import Flask, render_template
from reader import Reader

app = Flask(__name__)
reader = Reader()

@app.template_filter('format_byte_amount')
def format_byte_amount(num, suffix='B'):
    num = int(num)
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

@app.route("/")
def list_clients():
    return render_template('index.html', clients = reader.get_clients())

if __name__ == "__main__":
    app.run()
