import random
import json
import math
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


with open('content.json') as json_data:
    DATABASE = json.load(json_data)


def main():
    get_films()
    # message = str(input())
    # message = message.replace('ё', 'е')
    # print(calculate(message))



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
    
    
def calculate(message):
    answer = None
    numbers = []
    for num in message.split():
        try:
            numbers.append(float(num))
        except ValueError:
            pass
    if not numbers:
        return 'чота херня какаята'
    elif len(numbers) == 1 and ('факториал' in message or '!' in message):
        return math.factorial(numbers[0])
    print(numbers)
    try:
        if 'умнож' in message or '*' in message:
            answer = numbers[0] * numbers[1]
        elif 'дели' in message or '/' in message:
            answer = numbers[0] / numbers[1]
        elif 'плюс' in message or 'слож' in message or '+' in message:
            answer = numbers[0] + numbers[1]
        elif 'минус' in message or 'отним' in message or 'вычт' in message or '-' in message:
            answer = numbers[0] - numbers[1]
        elif 'остаток' in message or '%' in message:
            answer = numbers[0] % numbers[1]
    except IndexError:
        answer = 'чота херня какаята'
    if answer / int(answer) == 1:
        answer = int(answer)
    if answer > 999999999:
        return answer
    else:
        return round(answer, 3)


def get_films():
    current_film = None

    date = datetime.now() + timedelta(hours=3)
    date = date.strftime('%d.%m.%Y')
    resp = requests.get('http://afisha.360.by/category-films_schedule.html')
    soup = BeautifulSoup(resp.content, 'html.parser') 
    sub_soup = soup.body.section.select('.content > .items-block > .items-sub-block > .cinema_slider')[0]
    films = sub_soup.find_all('div', class_='item clearfix films', date=date)

    print(sub_soup)
    print(films)

    for film in films:
        sub_sub_soup = film.select('.cinemas-cell')[0]
        cinemas = sub_sub_soup.find_all('div', class_='item clearfix films')
        print(film.get('letter'))

    film_title = str(input())

    for film in films:
        if film_title.lower() in film.get('letter').lower():
            current_film = film
    
    
    print(current_film.find_next_sibling())
    
if __name__ == '__main__':
    main()