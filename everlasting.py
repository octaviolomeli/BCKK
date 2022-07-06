from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "This allows the bot to be online with repl.it closed"

def run():
  app.run(host='0.0.0.0',port=8080)

def everlasting():
    t = Thread(target=run)
    t.start()