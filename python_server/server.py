from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5000", "http://127.0.0.1:5000", "*"]}})

@app.route('/api/message', methods=['POST'])
def message():
    data = request.json
    url = data.get('url', '')

    

    response = f"Received: {url}"
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(port=5000)



