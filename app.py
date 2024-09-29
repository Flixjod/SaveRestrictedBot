from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Bot Alive'

@app.route('/health', methods=['GET'])
def health_check():
    return 'ok', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
