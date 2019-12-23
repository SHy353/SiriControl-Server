import socketio

# standard Python
sio = socketio.Client()
token = "e9491f80-a457-445e-a3b1-36d18f4e2e57"
sio.connect('http://localhost:5000?token=' + token)


@sio.on
def connect():
    print('Connected.')


@sio.on('commands')
def command(data):
    print(data)
    print("Command: ", data["command"])
    print("Option: ", data["option"])
    print("Spoken Text: ", data["spoken"])


@sio.on('lights')
def lights(data):
    print(data)
