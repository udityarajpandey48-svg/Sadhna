from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("/lemplates/index.html")

@app.route("/login")
def login():
    return render_template("/lemplates/login.html")


@app.route("/register")
def register():
    return render_template("/lemplates/register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)