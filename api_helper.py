import os
from dotenv import load_dotenv
import openai

player_name = None
player_description = None
player_attributes = None
player_image_link = None
DM_SYSTEM_COMMAND = None

default_attributes = { 'name': "Rognar, a barbarian",
'Strength': 6,
'Dexterity': 2,
'Constitution': 1,
'Intelligence': 1,
'Wisdom': 3,
'Charisma': 5}

DM_SYSTEM_COMMAND = {'role': 'system',
                     'content': f'''You are a dungeon master for a dungeons and dragons game. 
                     When I initially respond with "Where am I?", you will begin a solo campaign where the user is the 
                     following character:
---
{player_attributes if player_attributes else default_attributes}
---
As the Dungeon Master, you will progress the story based on the player's responses, working towards an eventual conclusion .

In each quest, you will set the scene for the player and give them the challenge to complete 

In the beginning, you will set the scene for the player, describe the situation, and allude to a larger mission.

In every subsequent quest after the first one, you should roll a die that works in tandem with one of the player's 
attributes to either help them progress or hamper their quest. The dice is 20 sided each roll is evaluated out of 20.

Make sure your message is complete and is never more than 175 words.
Ensure to be cognizant of the current and remaining states to create an intentional and complete resolution. 
The story should be of length remaining quests.'''}

def update_system_command(session_data):
    global DM_SYSTEM_COMMAND

    player_name = session_data.get('player_name')
    player_description = session_data.get('player_description')
    player_attributes = session_data.get('player_attributes')

    DM_SYSTEM_COMMAND = {'role': 'system',
                        'content': f'''You are a dungeon master for a dungeons and dragons game. 
                        When I initially respond with "Where am I?", you will begin a solo campaign where the user is the 
                        following character:
    ---
    Player Name: {player_name}
    Player Description: {player_description}
    {player_attributes}
    ---
    As the Dungeon Master, you will progress the story based on the player's responses, working towards an eventual conclusion .

    In each quest, you will set the scene for the player and give them the challenge to complete 

    In the beginning, you will set the scene for the player, describe the situation, and allude to a larger mission.

    In every subsequent quest after the first one, you should roll a die that works in tandem with one of the player's 
    attributes to either help them progress or hamper their quest. The dice is 20 sided each roll is evaluated out of 20.

    Make sure your message is complete and is never more than 175 words.
    Ensure to be cognizant of the current and remaining states to create an intentional and complete resolution. 
    The story should be of length remaining quests.'''}

    messages[0] = DM_SYSTEM_COMMAND


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
messages = [DM_SYSTEM_COMMAND]

def update_player_name(name):
    global player_name
    player_name = name

def update_player_description(desc):
    global player_description
    player_description = desc

def update_player_attributes(attrs):
    global player_attributes
    player_attributes = attrs


def get_dm_message(player_msg):
    """sends full user message to openai api. this should be done after processing the message"""
    openai.api_key = os.getenv("OPENAI_API_KEY_TEXT")

    message_obj = {'role': 'user', 'content': player_msg}
    messages.append(message_obj)

    # dm_response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo", messages=messages)

    dm_response = openai.ChatCompletion.create(
        model='gpt-4', messages=messages,
        temperature=0.7)
    dm_message = dm_response['choices'][0]['message']['content']

    return dm_message

# creates a prompt to feed into dall-e based on the dm response
def generate_prompt(dm_response):
    openai.api_key = os.getenv("OPENAI_API_KEY_TEXT")
    message_obj = {'role': 'user', 
                   'content': f'''extract lighting, location, and environment information from the following paragraph, make a DALLE prompt(natural language sentence) from it\n{dm_response}'''
                   }
    message_list = [message_obj]
    # messages.append(message_obj)
    model_engine = "gpt-3.5-turbo"
    completions = openai.ChatCompletion.create(
        model = model_engine,
        messages = message_list,
        max_tokens=20,
        temperature = 0.1
    )
    image_prompt = completions['choices'][0]['message']['content'] + ". In the style of a World of Warcraft game cg."
    return image_prompt

# creates a image based on image prompt
def generate_image(image_prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY_IMAGE")
    response = openai.Image.create(
        prompt=image_prompt,
        n = 1,
        size = "256x256"
    )
    return response['data'][0]['url']

def generate_character_prompt(description):
    openai.api_key = os.getenv("OPENAI_API_KEY_TEXT")
    message_obj = {'role': 'user', 
                   'content': f"imagine an description appearence of a character based on the description: {description if description else 'a barbarian'}"}
    message_list = [message_obj]
    # messages.append(message_obj)
    model_engine = "gpt-3.5-turbo"
    completions = openai.ChatCompletion.create(
        model = model_engine,
        messages = message_list,
        max_tokens=30,
        temperature = 0.8
    )
    character_prompt = completions['choices'][0]['message']['content'] + ". In the style of a hearthstone character."
    return character_prompt

def generate_character_image(character_prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY_IMAGE")
    response = openai.Image.create(
        prompt=character_prompt,
        n = 1,
        size = "256x256"
    )
    return response['data'][0]['url']

def transcribe(audio):
    openai.api_key = os.getenv("OPENAI_API_KEY_TEXT")
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

