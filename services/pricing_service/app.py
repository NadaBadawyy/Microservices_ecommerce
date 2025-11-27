from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Pricing Service Running!"

if __name__ == '__main__':
    app.run(port=5005, debug=True)
