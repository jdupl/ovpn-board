#!/usr/bin/env python3
from flask import Flask, render_template
from reader import Reader

app = Flask(__name__)
reader = Reader()

@app.route("/")
def list_clients():
    return render_template('index.html', clients = reader.get_clients())

if __name__ == "__main__":
    app.run()
