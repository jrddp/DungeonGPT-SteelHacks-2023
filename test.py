import api_helper
import sys

def test_generate_prompt(dm_response):
    result = api_helper.generate_prompt(dm_response)
    print(result)

def test_generate_image(image_prompt):
    link = api_helper.generate_image(image_prompt)
    print(link)

def test_generate_character_prompt(player_description):
    result = api_helper.generate_character_prompt(player_description)
    print(result)

def test_generate_character_image(character_prompt):
    link = api_helper.generate_character_image(character_prompt)
    print(link)

def main():
    tests = {"tgp": test_generate_prompt,
             "tgi": test_generate_image,
             "tgcp": test_generate_character_prompt,
             "tgci": test_generate_character_image,}
    if len(sys.argv) < 3:
        print("Test format error.")
        exit(1)
    test_name = sys.argv[1]
    test_input = sys.argv[2]
    print("-------------------- ")
    tests.get(test_name)(test_input)


if __name__ == "__main__":
    main()
