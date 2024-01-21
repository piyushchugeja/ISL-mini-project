import cv2
import numpy as np
import mediapipe as mp
import os
from gtts import gTTS
import playsound
from tensorflow.keras.models import load_model
from gemini import get_sentence

languages = {
    1: ['English', 'en'],
    2: ['Hindi', 'hi'],
}

print()
for i in languages:
    print(i, "-", languages[i][0])
lang_i = int(input("\nSelect your language: "))
lang = languages[lang_i][0]
language = languages[lang_i][1]

def speak(sentence):
    try:
        response = gTTS(text=sentence, lang=language)
        if (os.path.exists("response.mp3")):
            os.remove("response.mp3")
        response.save("response.mp3")
        playsound.playsound("response.mp3", True)
        os.remove("response.mp3")
    except:
        print("Error while speaking, please try again later.")

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

model = load_model('mp_hand_gesture')

f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()

cap = cv2.VideoCapture(0)
predicted_words = []
processing = False

while True:
    _, frame = cap.read()
    x, y, c = frame.shape
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    className = ''
    if result.multi_hand_landmarks and not processing:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]
            if predicted_words == [] or predicted_words[-1] != className:
                predicted_words.append(className)
    else:
        if predicted_words != [] or len(predicted_words) > 1:
            print("\nList of words:", predicted_words)
            # sentence = run_request(predicted_words, language)
            sentence = get_sentence(predicted_words, lang)
            print("Sentence:", sentence)
            predicted_words = []
            speak(sentence)
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Output", frame) 
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()