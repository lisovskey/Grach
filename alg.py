import random
import json

with open('content.json') as json_data:
    DATABASE = json.load(json_data)
    
text_message = str(input())

parts = 0
word = None
no_commands = True
need_name = 0

if any(name in text_message for name in DATABASE['config']['bot_names']):
    need_name = 1
for command in DATABASE['commands']:
    for text in command['text']:
        if type(text) is dict:
            for word in text['part']:
                if word in text_message:
                    i = text_message.find(word)
                    if (i + len(word)) < len(text_message):
                        if text_message[i + len(word)] != "\a" or text_message[i + len(word) + 2] != "\s":
                            parts += 1
                            break
                    elif (i + len(word)) == len(text_message):
                        parts += 1
                        break
        else:
            print(text)
    if need_name > 0:
        if parts == command['parts']:
            no_commands = False
            print(random.choice(command['answer']))
    parts = 0
if no_commands and need_name > 0:
    print(random.choice(DATABASE['config']['bot_call_output']))
