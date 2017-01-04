import random
import json

with open('content.json') as json_data:
    DATABASE = json.load(json_data)
    
text_message = str(input())


for command in DATABASE['commands']:
        if command['text'] in text_message:
            exec(command['answer'])