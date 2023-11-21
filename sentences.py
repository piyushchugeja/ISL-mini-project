import websocket
import json
import os

chatId = os.urandom(16).hex()

url = "wss://backend.buildpicoapps.com/api/chatbot/chat"

websocket.enableTrace(False) 
ws = websocket.WebSocketApp(url)
systemPrompt = "You will be given a set of words, generate a grammatically correct sentence using those words. Return only the sentence and nothing more.";
message = ''

def on_open(ws):
    payload = {
        "chatId": chatId,
        "appId": "dark-pay",
        "systemPrompt": systemPrompt,
        "message": message,
    }
    ws.send(json.dumps(payload))

sentence = ''

def on_message(ws, message):
    global sentence
    sentence += message

def run_request(words, language):
    global sentence, message
    sentence = ''
    message = 'Words: '+ ', '.join(words) + '. \nUse language: ' + language + '.'
    ws.on_open = on_open
    ws.on_message = on_message
    ws.run_forever()
    ws.close()
    return sentence