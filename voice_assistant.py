import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import smtplib
import ssl

# ✅ Set Chrome as the default browser
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# ✅ Initialize recognizer and voice engine
listener = sr.Recognizer()
engine = pyttsx3.init()
listener.pause_threshold = 1  # waits for pause in speech

# ✅ Voice speaking function
def talk(text):
    print("🗣️ Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ✅ Listen to user voice
def listen_command():
    try:
        with sr.Microphone() as source:
            print("🎤 Listening... Speak now!")
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"🧠 You said: {command}")
    except sr.WaitTimeoutError:
        command = ""
        print("⌛ You took too long to speak.")
    except sr.UnknownValueError:
        command = ""
        print("🤷 I couldn't understand your speech.")
    except sr.RequestError:
        command = ""
        print("❌ Could not reach Google's servers (internet issue).")
    return command

# ✅ Email contacts and credentials
contacts = {
    "ram": "ruascomrade@gmail.com",
    "kiran": "pukudent342@gmail.com"
}

your_email = "chinmaysahithvankadaru@gmail.com"
app_password = "igmi qota ujrt hgrd"  # 🔐 Replace with actual app password

# ✅ Get email from name
def get_email(name):
    return contacts.get(name.lower(), None)

# ✅ Send email using Gmail SMTP
def send_email(receiver_email, subject, message):
    try:
        email_text = f"Subject: {subject}\n\n{message}"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(your_email, app_password)
            server.sendmail(your_email, receiver_email, email_text)
        talk("✅ Email sent successfully.")
    except Exception as e:
        print(f"[DEBUG] Error sending email: {e}")
        talk("❌ Failed to send email.")

# ✅ Send WhatsApp Message
def send_whatsapp():
    whatsapp_contacts = {
        "saico": "+918106725469",
        "go": "+917981869172",
        "jayanth": "+916305375030"
    }

    talk("Who do you want to message?")
    name_or_number = listen_command()

    number = ""
    if name_or_number in whatsapp_contacts:
        number = whatsapp_contacts[name_or_number]
    elif name_or_number.startswith("plus") or name_or_number.startswith("+"):
        number = name_or_number.replace(" ", "").replace("plus", "+")
    else:
        talk("I don't have that contact saved. Please use full number with country code.")
        return

    talk("What is your message?")
    message = listen_command()

    if message:
        talk(f"Sending your message: {message}")
        pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
    else:
        talk("I didn’t catch the message.")

# ✅ MAIN ASSISTANT FLOW
print("Say something after the beep...")
talk("Hi, I am your assistant. What can I do for you?")
command = listen_command()

if 'hello' in command:
    talk("Hello! How are you?")
elif 'your name' in command:
    talk("I am your voice assistant.")
elif 'open youtube' in command:
    talk("Opening YouTube for you.")
    webbrowser.get('chrome').open("https://www.youtube.com")
elif 'search' in command:
    talk("What do you want me to search?")
    search_query = listen_command()
    if search_query:
        talk(f"Searching for {search_query}")
        webbrowser.get('chrome').open(f"https://www.google.com/search?q={search_query}")
    else:
        talk("I didn't get the search keyword.")
elif 'send whatsapp' in command or 'whatsapp' in command:
    send_whatsapp()
elif 'play' in command:
    song = command.replace('play', '').strip()
    talk(f"Playing {song} on YouTube.")
    pywhatkit.playonyt(song)
elif 'send email' in command or 'send mail' in command:
    talk("You can say something like: 'Send email to Kiran'. Now tell me — who should I send the email to?")
    name_input = listen_command()
    
    # 🧠 Clean the voice input
    name = name_input.replace("send email to", "").replace("to", "").strip()
    
    email = get_email(name)
    if email:
        talk("What is the subject?")
        subject = listen_command()
        talk("What is the message?")
        message = listen_command()
        send_email(email, subject, message)
    else:
        talk(f"Sorry, I couldn’t find an email for {name}.")
else:
    talk("Sorry, I didn't understand that.")
