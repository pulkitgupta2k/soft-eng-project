from flask import Flask, request, render_template, redirect, url_for, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", **locals())

if __name__ == "__main__":
    app.run(debug='true', host='127.0.0.1', port='5000')