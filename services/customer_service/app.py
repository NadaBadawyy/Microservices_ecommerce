from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Customer Service Running!"

if __name__ == '__main__':
    app.run(port=5003, debug=True)