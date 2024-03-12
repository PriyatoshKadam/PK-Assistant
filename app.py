from flask import Flask, render_template, request, jsonify
import datetime
import webbrowser
import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr 
import wikipedia
import smtplib

app = Flask(__name__, static_url_path='/static')
listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json['command']
    response = run_john(command)
    return jsonify({'response': response})

@app.route('/voice_input')
def voice_input():
    command = take_command()
    return jsonify({'command': command})

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def take_command():
    try:
        with sr.Microphone() as source:
            print('John is listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'john' in command:
                command = command.replace('john', '')
                print(command)
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that. Can you please repeat?")
        return take_command()
    except sr.RequestError:
        talk("Sorry, I'm having trouble accessing the recognition service.")
        return ""
    return command

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("justforcode04@gmail.com", '***')  
        server.sendmail('yashmahi0404@gmail.com', to, content) 
        server.close()
        talk("Email has been sent successfully.")
    except Exception as e:
        print(e)
        talk("Sorry, I am unable to send this email.")

def run_john(command):
    wish = wish_me()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)
    elif 'tell me about' in command:
        topic = command.replace('tell me about', '')
        try:
            info = wikipedia.summary(topic, sentences=2)
            print(info)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find information on that topic.")
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
    elif 'open youtube' in command:
        webbrowser.open('https://youtube.com')
    elif 'open google' in command:
        webbrowser.open('https://google.com')
    elif 'news' in command:
        talk("Here are the latest news")
        webbrowser.open('https://news.google.co.in')
    elif 'music' in command:
        talk("Sure, let's listen to some music.")
        webbrowser.open('https://soundcloud.com')
    elif 'search' in command:
        talk('Yes, I can surely do it. What should I search for?')
        search = take_command()
        url = 'https://google.com/search?q=' + search
        webbrowser.open(url)
        talk('Here is what I found for ' + search)
    elif "send email" in command:
        talk("Whom do you want to send the email to?")
        to = take_command()
        talk("What should I say in the email?")
        content = take_command()
        send_email(to, content)
    else:
        return "I didn't get you, please repeat."

if __name__ == '__main__':
    app.run(debug=True)