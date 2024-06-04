import os
import io
import json
import requests
import spacy
import pyaudio
import wave
from google.cloud import speech

# Set up Google Cloud Speech-to-Text client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_google_cloud_credentials.json"
client = speech.SpeechClient()

# Set up spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def transcribe_audio():
    with io.open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=RATE, language_code="en-US")
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript
    return ""

def process_text(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity, i.e., location
            return get_weather(ent.text)
    return "Sorry, I didn't understand that."

def get_weather(location):
    api_key = "your_openweather_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={location}&appid={api_key}"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The temperature in {location} is {temperature - 273.15:.2f}°C with {weather_desc}."
    else:
        return "City not found."

def main():
    record_audio()
    text = transcribe_audio()
    if text:
        print(f"Recognized Text: {text}")
        response = process_text(text)
        print(response)
    else:
        print("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()
