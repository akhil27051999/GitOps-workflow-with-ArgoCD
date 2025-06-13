from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Welcome to the GitOps Flask App!"

@app.route("/healthz")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

