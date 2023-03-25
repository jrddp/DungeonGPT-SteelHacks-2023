from flask import Flask, render_template, request, redirect, url_for, jsonify
import openai

from api_helper import get_dm_message, generate_prompt, generate_image, transcribe

app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json'

@app.route('/', methods=['GET', 'POST'])
def gameplay():
    if request.method == 'POST':
        print(request.mimetype)
        if request.is_json:
            data = request.get_json()
            player_response = data.get("player_response")
            return get_dm_message_json(player_response)
        else:
            # Handle non-AJAX form submission (if needed)
            dungeon_master_message = "This should not happen..."
            pass
    else:
        # First-time rendering or initial state
        dungeon_master_message = "Welcome to the AI-powered dungeon game!"
    return render_template('gameplay.html', dungeon_master_message=dungeon_master_message)


@app.route('/process-audio', methods=['POST'])
def process_audio():
    audio = request.files['audio']
    player_message = transcribe(audio)
    return get_dm_message_json(player_message)


def get_dm_message_json(player_message):
    dungeon_master_message = get_dm_message(player_message)
    return jsonify({"dungeon_master_message": dungeon_master_message})


if __name__ == '__main__':
    app.run(debug=True)
