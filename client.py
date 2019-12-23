import socketio

sio = socketio.Client()

# Replace with your generated token
token = "a598fbce-7cc7-4240-ad35-0b86b2651c59"
sio.connect('https://siricontrol-server.herokuapp.com:5000/?token=' + token)


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
