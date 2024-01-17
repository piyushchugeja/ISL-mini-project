import google.generativeai as genai
import os
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel("gemini-pro")

def get_sentence(words, language):
    prompt = "You are being given a set of words, generate a grammatically correct and meaningful sentence using those words. Do not add context to the sentence. Return only the sentence and nothing more. \nWords: " + ', '.join(words) + ". \nUse language: " + language + "."
    response = model.generate_content(
        prompt,
    )
    print(response.text)
    return response.text