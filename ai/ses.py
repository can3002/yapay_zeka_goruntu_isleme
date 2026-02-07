from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
import os
import time
from datetime import datetime
import webbrowser

r = sr.Recognizer()

# 1. Recognizer ayarlarını optimize edin
r.energy_threshold = 300  # Daha düşük = daha hassas (varsayılan ~4000)
r.dynamic_energy_threshold = True  # Otomatik ayarlama
r.pause_threshold = 0.8  # Duraklamadan önce bekleme süresi (saniye)


def record(prompt=None, timeout=10, phrase_limit=10):
    with sr.Microphone() as source:
        # 2. Ambient noise ayarını artırın
        r.adjust_for_ambient_noise(source, duration=1)  # 0.5'ten 1'e çıkarın

        if prompt:
            print(prompt)

        try:
            # 3. Google tanıma ayarlarını iyileştirin
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

            # show_all=True ile alternatifleri görün
            voice = r.recognize_google(
                audio,
                language="tr-TR",
                show_all=False  # True yaparsanız alternatifleri görebilirsiniz
            )
            print(f"Algılanan: {voice}")
            return voice

        except sr.WaitTimeoutError:
            print("Asistan: Dinleme zaman aşımı")
        except sr.UnknownValueError:
            print("Asistan: Anlayamadım, tekrar söyler misin?")
        except sr.RequestError as e:
            print(f"Asistan: Sistem çalışmıyor - {e}")
        return ""


# ======================
# KONUŞMA
# ======================
def speak(text):
    print(f"Asistan: {text}")
    tts = gTTS(text=text, lang="tr", slow=False)
    file = "voice.mp3"
    tts.save(file)
    playsound(file)
    os.remove(file)


# ======================
# KOMUTLAR
# ======================
def response(voice):
    voice = voice.lower()

    if "merhaba" in voice:
        speak("Sana da merhaba genç")

    elif "selamun aleyküm" in voice or "selam" in voice:
        speak("Aleyküm selam")

    elif "teşekkürler" in voice or "teşekkür" in voice:
        speak("Rica ederim")
        exit()

    elif "görüşürüz" in voice or "kapat" in voice or "kapanabilirsin" in voice:
        speak("Görüşmek üzere")
        exit()

    elif "hangi gündeyiz" in voice or "bugün ne günü" in voice:
        days = {
            "Monday": "Pazartesi",
            "Tuesday": "Salı",
            "Wednesday": "Çarşamba",
            "Thursday": "Perşembe",
            "Friday": "Cuma",
            "Saturday": "Cumartesi",
            "Sunday": "Pazar"
        }
        today = days[datetime.now().strftime("%A")]
        speak(f"Bugün {today}")

    elif "saat kaç" in voice:
        clock = datetime.now().strftime("%H:%M")
        speak(f"Saat şu an {clock}")

    elif "google" in voice:
        speak("Ne aramamı istiyorsun?")
        search = record(timeout=7, phrase_limit=7)

        if "görsel" in search or "resim" in search:
            # Görselden arama için tbm=isch parametresi
            webbrowser.open(f"https://www.google.com/search?tbm=isch&q={search}")


        elif "alışveriş" in search or "shopping" in search:
            # Alışveriş araması için tbm=shop parametresi
            webbrowser.open(f"https://www.google.com/search?tbm=shop&q={search}")


        elif "harita" in search or "konum" in search or "nerede" in search:
            # Harita/konum araması için Google Maps
            webbrowser.open(f"https://www.google.com/maps/search/{search}")


        elif search:
            webbrowser.open(f"https://www.google.com/search?q={search}")


    elif "youtube" in voice:
        speak("Youtube'u açıyorum")
        webbrowser.open("https://www.youtube.com")
        time.sleep(2)
        speak("Ne aramamı istersin?")
        search = record(timeout=7, phrase_limit=7)
        if search:
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={search.replace(' ', '+')}"
            )
            speak(f"{search} için sonuçları açıyorum")

    elif "uygulama aç" in voice or "aç" in voice:
        speak("Hangi uygulamayı açmamı istiyorsun?")
        app = record(timeout=7, phrase_limit=7).lower()

        if "valorant" in app:
            os.startfile(r"D:\Riot Games\Riot Client\RiotClientServices.exe")
            speak("Valorant açılıyor")
        else:
            speak("Bu uygulama listemde yok")
    elif "Kapanabilirsin" in voice:
        exit()
    else:
        speak("Bu komutu anlayamadım")


# ======================
# BAŞLANGIÇ
# ======================
speak("İyi günler efendim nasıl yardımcı olabilirim")

while True:
    print("\n--- Komut bekleniyor ---")
    command = record(timeout=10, phrase_limit=10)

    if command:
        response(command)
        time.sleep(0.5)