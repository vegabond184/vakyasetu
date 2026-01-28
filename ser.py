from flask import Flask
import hcs
import pyautogui

app = Flask(__name__)

@app.route('/')
def matrixmovement():
    pyautogui.press('Delete')
    return "hello"

@app.route('/enter')
def _enter():
    pyautogui.press('enter')
    return "enter"

@app.route("/selection")
def selection():
    pyautogui.press('down')
    return 'selection'

@app.route("/done")
def done():
    hcs.speak("Device connected")
    return "done"


if "__main__" == __name__:
    app.run(host="0.0.0.0", debug = True)