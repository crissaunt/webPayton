from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SocketIO with CORS
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for WebSocket

connected_users = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("location")
def handle_location(data):
    user_id = request.sid  # Unique session ID
    connected_users[user_id] = {
        'lat': data['lat'],
        'lon': data['lon'],
        'timestamp': data['timestamp'],
        'user_id': user_id
    }
    emit('update', connected_users[user_id], broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    if user_id in connected_users:
        emit('user_disconnected', {'user_id': user_id}, broadcast=True)
        del connected_users[user_id]

if __name__ == "__main__":
   socketio.run(app, host="0.0.0.0", port=8080, debug=True)  # Disable debug mode
