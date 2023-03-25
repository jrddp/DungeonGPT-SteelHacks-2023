import os
from flask import Flask, redirect, render_template, request, jsonify, url_for, send_file

import azure.cognitiveservices.speech as speechsdk


from api_helper import (get_dm_message, generate_prompt, generate_image,
                        generate_character_prompt, generate_character_image,
                        transcribe, update_player_attributes,
                        update_player_description, update_player_name, update_system_command)


app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json'

speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SPEECH_REGION")

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)
audio_config = speechsdk.audio.AudioOutputConfig(
    filename=".tmp/textSpeech.wav")
# speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

speech_config.speech_synthesis_language = "en-US"
speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"


@app.route("/synthesize_speech", methods=["POST"])
def synthesize_speech():
    print("Synthesizing speech...")
    print(request.get_json())
    text = request.get_json()['text']
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text(text)
    state = "done"
    return jsonify({"state": state})


@app.route('/get-audio')
def get_audio():
    return send_file('.tmp/textSpeech.wav', mimetype='audio/wav')


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
        global player_description
        global player_name
        print(request.form)
        data = request.form
        player_name = data['player_name']
        player_description = data['player_description']
        strength = data['strength']
        dexterity = data['dexterity']
        constitution = data['constitution']
        intelligence = data['intelligence']
        wisdom = data['wisdom']
        charisma = data['charisma']
        input_attributes = {'name': player_name,
                            'strength': strength,
                            'dexterity': dexterity,
                            'constitution': constitution,
                            'intelligence': intelligence,
                            'wisdom': wisdom,
                            'charisma': charisma}

        update_player_name(player_name)
        update_player_description(player_description)
        update_player_attributes(input_attributes)
        update_system_command()
        return redirect(url_for("gameplay"))
    else:
        return render_template('character_creation.html')


@app.route('/player_image', methods=['POST'])
def player_image():
    image_link = update_player_image_link(player_description)
    return jsonify({"player_image": image_link})


def update_player_image_link(description):
    character_prompt = generate_character_prompt(description)
    player_image_link = generate_character_image(character_prompt)
    return player_image_link


def get_dm_message_json(player_message):
    dungeon_master_message = get_dm_message(player_message)
    return jsonify({"dungeon_master_message": dungeon_master_message})


def get_state_image_link_json(dungeon_master_message):
    image_prompt = generate_prompt(dungeon_master_message)
    image_link = generate_image(image_prompt)
    return jsonify({"state_image": image_link})


if __name__ == '__main__':
    app.run(debug=True)
