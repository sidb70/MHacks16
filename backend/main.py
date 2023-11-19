from speech.TextToVoice import convert_to_voice
from speech.VoiceToText import transcribe
from therapy import get_therapist_message, post_user_message, add_emotion
from flask import Flask, jsonify, request, send_file,render_template,send_file
from vision.emotions import get_emotion_from_image
from flask_cors import CORS
import os
import base64

app = Flask(__name__)
CORS(app)  

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': "Reached Server!"})

@app.route('/posttext', methods=['POST'])
def handle_text_input():
    try:
        user_text = request.json['userText']
        post_user_message(user_text, use_emotion=False)              #give the chatgpt 
        therapist_text = get_therapist_message()       

        convert_to_voice(therapist_text)

        directory_path = os.path.join(os.getcwd(), "backend", "speech", "out", "output.mp3")

        return send_file(directory_path, as_attachment=True)
    except Exception as e:
        print("Are you sure you provided an MP3?")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/postinput', methods=['POST'])
def handle_recorded_input():
    try:
        audio_file = request.files['audioFile']
        photo_file = request.files['photo']

        # Process the audio file
        with open('backend/speech/in/user_response.mp3', 'wb') as f:
            f.write(audio_file.read())

        # Process the photo file
        with open('backend/vision/in/user_image.jpg', 'wb') as f:
            f.write(photo_file.read())

        emotion, likelihood = get_emotion_from_image('backend/vision/in/user_image.jpg')
        add_emotion(emotion)

        user_text = transcribe('backend/speech/in/user_response.mp3')
        post_user_message(user_text, use_emotion=True)              #give the chatgpt 
        therapist_text = get_therapist_message()       

        convert_to_voice(therapist_text)

        directory_path = os.path.join(os.getcwd(), "backend", "speech", "out", "output.mp3")
        print(directory_path)

        return send_file(directory_path, as_attachment=True)
    except Exception as e:
        print("Are you sure you provided an MP3?")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__": 
    #app.run(host = '127.0.0.1', port = 5000)
    app.run()