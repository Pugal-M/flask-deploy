from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/greet", methods=["GET"])
def greet():
    return jsonify({"message": "Hello from Python backend!"})

if __name__ == "__main__":
    app.run()



