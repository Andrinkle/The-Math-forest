import speech_recognition as sr
import whisper
from os import remove as os_remove
import threading
import keyboard


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model("base")
        self.audio = None
        self.text = ""
        self.recording = False

    def record_audio(self):
        "Запись аудио с микрофона с возможностью ручной остановки."
        self.recording = True

        def listen():
            with sr.Microphone() as source:
                print("Запись началась. Нажмите 'q', чтобы остановить.")
                self.recognizer.adjust_for_ambient_noise(source)
                self.audio = self.recognizer.listen(source, phrase_time_limit=None)

        # Создаём поток для записи
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

        # Ожидаем нажатия клавиши 'q' для остановки записи
        keyboard.wait("q")
        self.recording = False
        print("Запись остановлена.")

    def recognize_speech(self, save_to_file: bool = False):
        "Преобразование аудио в текст с помощью Whisper"
        # Сохранение аудио в файл для обработки
        with open("output.wav", "wb") as f:
            f.write(self.audio.get_wav_data())
        
        # Транскрибация файла в текст
        self.text = self.model.transcribe("output.wav")['text']
        print("Распознанный текст:", self.text)


sp_to_t = SpeechToText()
sp_to_t.record_audio()
sp_to_t.recognize_speech()
