import random
import json

with open('content.json') as json_data:
    DATABASE = json.load(json_data)


def main():
    calculate()



def search_command():
    text_message = str(input()) + ' '
    text_message = text_message.replace('ё', 'е')
    parts = 0
    word = None
    no_commands = True
    need_name = 0

    if any(name in text_message for name in DATABASE['config']['bot_names']):
        need_name = 1
    for command in DATABASE['commands']:
        for text in command['text']:
            for word in text['part']:
                if word in text_message:
                    right = True
                    i = text_message.find(word)
                    length = text_message.find(' ', i)
                    for exception in command['exceptions']:
                        print(exception)
                        print(text_message[i:length])
                        if exception in text_message[i: length]:
                            right = False
                            break
                    if right:
                        parts += 1
                        break
        '''for word in text['part']:
            print(word)
                if word in text_message:
                    i = text_message.find(word)
                    if (i + len(word)) < len(text_message):
                        if text_message[i + len(word) + 1] == ' ':
                            parts += 1
                            break
                    elif (i + len(word)) == len(text_message):
                        parts += 1
                        break'''
        if need_name > 0:
            if parts == command['parts']:
                no_commands = False
                print(random.choice(command['answer']))
        parts = 0
    if no_commands and need_name > 0:
        print(random.choice(DATABASE['config']['bot_call_output']))
    
    
def calculate():
    text_message = str(input()) + ' '
    text_message = text_message.replace('ё', 'е')
    words = text_message.split()
    numbers = []
    num_index = []
    for num in words:
        try:
            numbers.append(float(num))
            num_index.append(words.index(num))
        except ValueError:
            pass
    
    print(num_index)
    print(numbers)
    print(words)

    
    
if __name__ == '__main__':
    main()