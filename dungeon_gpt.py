import io
import os
from flask import Flask, render_template, request, jsonify
import base64

import azure.cognitiveservices.speech as speechsdk


from api_helper import get_dm_message, generate_prompt, generate_image, transcribe

app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json'

speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SPEECH_REGION")

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

speech_config.speech_synthesis_language = "en-US"
speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"


@app.route("/synthesize_speech", methods=["POST"])
def synthesize_speech():
    print("Synthesizing speech...")
    print(request.get_json())
    text = request.get_json()['text']
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text_async(text)
    return ""

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/play', methods=['GET', 'POST'])
def gameplay():
    # print(f"Received request: {request.method}")

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            player_response = data.get("player_response")
            return get_dm_message_json(player_response)
        else:
            # Handle non-AJAX form submission
            dungeon_master_message = "Invalid request received."
    else:
        # First-time rendering or initial state
        dungeon_master_message = "Welcome to the AI-powered dungeon game!"
    return render_template('gameplay.html', dungeon_master_message=dungeon_master_message)


@app.route('/process-image', methods=['POST'])
def process_image():
    if request.is_json:
        data = request.get_json()
        dm_message = data.get("dungeon_message")
        image_link = get_state_image_link_json(dm_message)
        return image_link


@app.route('/process-audio', methods=['POST'])
def process_audio():
    audio = request.files['audio']
    player_message = transcribe(audio)
    return get_dm_message_json(player_message)


@app.route('/character_creation', methods=['GET', 'POST'])
def character_creation():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            archetype = data.get('archetype')
            strength = data.get('strength')
            dexterity = data.get('dexterity')
            constitution = data.get('constitution')
            intelligence = data.get('intelligence')
            wisdom = data.get('wisdom')
            charisma = data.get('charisma')
            player_attributes = {'name': name,
                                'archetype': archetype,
                                'strength': strength,
                                'dexterity': dexterity,
                                'constitution': constitution,
                                'intelligence': intelligence,
                                'wisdom': wisdom,
                                'charisma': charisma}
        else:
            player_attributes = {'name': 'Invalid request received.'}
        return jsonify({"player_attributes": player_attributes})
    else:
        return render_template('character_creation.html')


def get_dm_message_json(player_message):
    dungeon_master_message = get_dm_message(player_message)
    return jsonify({"dungeon_master_message": dungeon_master_message})


def get_state_image_link_json(dungeon_master_message):
    image_prompt = generate_prompt(dungeon_master_message)
    image_link = generate_image(image_prompt)
    return jsonify({"state_image": image_link})


if __name__ == '__main__':
    app.run(debug=True)
