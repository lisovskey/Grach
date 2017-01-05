import random
import json

with open('content.json') as json_data:
    DATABASE = json.load(json_data)
    
text_message = str(input())


flag = False
word = None

'''command = DATABASE['commands'][0]
print(command)
text_list = command['text']
print(text_list)
text = text_list[0]
print(text)
word = text['part']
print(word)
word = word[0]
print(word)
''' 
for command in DATABASE['commands']:
    for text in command['text']:
        if type(text) is dict:
            for word in text['part']:
                if word in text_message:
                    flag = True
                    break
                else:
                    flag = False
        else:
            print(text)
    # if any(name in text_message for name in DATABASE['config']['bot_names']):
    if flag:
        print(random.choice(command['output']))
        flag = False
        break
#    else:
#        print(random.choice(DATABASE['config']['bot_call_output']))
        
        