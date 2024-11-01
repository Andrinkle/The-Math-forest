import speech_recognition as sr
import whisper
from os import remove as os_remove


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model("base")
        self.audio = None
        self.text = ""


    def record_audio(self):
        "Запись аудио с микрофона."
        with sr.Microphone() as source:
            print("Запись аудио")
            self.recognizer.adjust_for_ambient_noise(source)
            self.audio = self.recognizer.listen(source)


    def recognize_speech(self, save_to_file:bool=False):
        "Процесс захвата аудио, с возможностью сохранения и преобразования в текст."
        with open("output.wav", "wb") as f:
            f.write(self.audio.get_wav_data())
        # Транскрибация аудиофайла в текст с помощью Whisper
        self.text = self.model.transcribe("output.wav")
        if not save_to_file:
            os_remove("output.wav")

sp_to_t = SpeechToText()
sp_to_t.record_audio()
sp_to_t.recognize_speech()
print(sp_to_t.text)
