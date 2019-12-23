from flask import Flask, request
from flask_socketio import SocketIO
import os
import json
from main import SiriControl
import keepAlive

app = Flask(__name__)
socket = SocketIO(app)


@app.route('/')
def main():
    return "SiriControl is running"


def authenticate(token):
    if token != os.getenv("SECRETID"):
        return False
    else:
        return True


@socket.on('connect')
def connect():
    if not authenticate(request.args.get("token")):
        raise ConnectionRefusedError('unauthorized')


with open("commands.json", 'r') as f:
    commands = json.loads(f.read())['commands']


def parseCommand(spokenText):
    userCommand = False
    userOption = False
    for command in commands:

        foundWords = []
        for word in commands[command]['required']:
            if word in spokenText:
                foundWords.append(word)

        if(len(foundWords) == len(commands[command]['required'])):
            userCommand = command

        for option in commands[command]['options']:
            if option in spokenText:
                userOption = option

    return userCommand, userOption


def callback(spokenText):
    command, option = parseCommand(spokenText)
    if command:
        print("The word(s) '" + spokenText + "' have been said")
        print("Command: ", command, ", Option: ", option)
        socket.emit('commands', {"spoken": spokenText,
                                 "command": command, "option": option})
        socket.emit(command, {"spoken": spokenText, "option": option})


if __name__ == '__main__':
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")

    if (username == None or password == None):
        print("No username or password found. Please set these environment variables.")
    else:
        # keepAlive.start()
        c = SiriControl(callback, username, password)
        c.start()
        socket.run(app, debug=False, host="0.0.0.0", port=os.getenv("PORT"))
