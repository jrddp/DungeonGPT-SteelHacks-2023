import os
from dotenv import load_dotenv
import openai

player_attributes = { 'name': "Rognar, a barbarian",
'Strength': 6,
'Dexterity': 2,
'Constitution': 1,
'Intelligence': 1,
'Wisdom': 3,
'Charisma': 5}

DM_SYSTEM_COMMAND = {'role': 'system',
                     'content': f'''You are a humorous dungeon master for a dungeons and dragons game. 
                     When I initially respond with "Where am I?", you will begin a solo campaign where the user is the 
                     following character:
---
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

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
messages = [DM_SYSTEM_COMMAND]



#Get players attributes including name attribute values and et al

def player_attributes(player_msg):
    #todo implement
    return player_msg


def decorate_player_message(player_msg):
    """Uses gpt to determine relevant stat and add roll to the end of the player's original message"""
    # todo implement
    return player_msg

def get_dm_message(player_msg):
    """sends full user message to openai api. this should be done after processing the message"""
    openai.api_key = os.getenv("OPENAI_API_KEY_TEXT")

    message_obj = {'role': 'user', 'content': player_msg}
    messages.append(message_obj)

    dm_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)

    # dm_response = openai.ChatCompletion.create(
    #     model='gpt-4', messages=messages)
    dm_message = dm_response['choices'][0]['message']['content']

    return dm_message

# creates a prompt to feed into dall-e based on the dm response
def generate_prompt(dm_response):
    openai.api_key = os.getenv("OPENAI_API_KEY_TEXT")
    message_obj = {'role': 'user', 
                   'content': f'''extract lighting, location, and environment information from the following paragraph, make a DALLE prompt from it, example: a town in the style of a World of Warcraft screenshot\n{dm_response}'''
                   }
    messages.append(message_obj)
    model_engine = "gpt-3.5-turbo"
    completions = openai.ChatCompletion.create(
        model = model_engine,
        messages = messages,
        max_tokens=20,
        temperature = 0.1
    )
    image_prompt = completions['choices'][0]['message']['content'] + "In the style of a World of Warcraft screenshot"
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

def transcribe(audio):
    openai.api_key = os.getenv("OPENAI_API_KEY_TEXT")
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

