from gtts import gTTS
import playsound, os
text = 'Hello, this is from India'
response = gTTS(text=text, lang="en", tld="co.in")
response.save("response.mp3")
playsound.playsound("response.mp3", True)
os.remove("response.mp3")