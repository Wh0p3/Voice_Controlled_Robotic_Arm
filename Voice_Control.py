import serial
import speech_recognition as sr

arduino = serial.Serial('COM21', 9600, timeout=1)

current_angles = {
    "base": 90,
    "elbow": 90,
    "shoulder": 90
}

def send_angles_to_arduino(angles):
    command = f"{int(angles['base'])} {int(angles['shoulder'])} {int(angles['elbow'])}\n"
    arduino.write(command.encode())
    print("Sent to Arduino:", command)

def process_command(keywords_found):
    global current_angles
    movement_amount = 20

    if "up" in keywords_found:
        current_angles["shoulder"] += movement_amount
    if "down" in keywords_found:
        current_angles["shoulder"] -= movement_amount
    if "left" in keywords_found:
        current_angles["base"] -= movement_amount
    if "right" in keywords_found:
        current_angles["base"] += movement_amount
    if "forward" in keywords_found:
        current_angles["elbow"] -= movement_amount
    if "backward" in keywords_found:
        current_angles["elbow"] += movement_amount

    current_angles["base"] = max(0, min(180, current_angles["base"]))
    current_angles["shoulder"] = max(0, min(180, current_angles["shoulder"]))
    current_angles["elbow"] = max(0, min(180, current_angles["elbow"]))

    send_angles_to_arduino(current_angles)

recognizer = sr.Recognizer()
keywords = ["up", "down", "forward", "backward", "left", "right", "pick", "drop"]

def get_voice_command():
    with sr.Microphone() as source:
        print("Listening for commands via laptop microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="en-IN")
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def find_keywords(command):
    found_keywords = [keyword for keyword in keywords if keyword in command]
    return found_keywords

while True:
    voice_command = get_voice_command()
    if voice_command:
        keywords_found = find_keywords(voice_command)
        if keywords_found:
            print(f"Found keywords: {', '.join(keywords_found)}")
            process_command(keywords_found)
        else:
            print("No keywords found in the command.")