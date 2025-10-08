# /flask_backend/app.py
from flask import Flask, request, Response
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/twilio-call", methods=["POST"])
def twilio_call():
    twiml = """
    <Response>
      <Start>
        <Stream url="wss://concavely-inflationary-eddy.ngrok-free.dev/ws"/>
      </Start>
      <Say>Welcome to SafePal scam protection!</Say>
      <Pause length="120"/>
    </Response>
    """
    return Response(twiml, mimetype='text/xml')

@socketio.on('connect')
def test_connect():
    print('WebSocket client connected')

@socketio.on('media')
def handle_media(data):
    print("Received media packet:", data)

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    socketio.run(app, host="0.0.0.0", port=5000)

