from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Notification Service Running!"

if __name__ == '__main__':
    app.run(port=5002, debug=True)
