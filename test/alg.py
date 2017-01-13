import random
import math
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def main():
    get_films()
    
    
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
    films = soup.find_all('div', class_='item clearfix films', date=date)

    for film in films:
        print(film.get('letter'))

    film_title = str(input())
    
    for film in films:
        if film_title.lower() in film.get('letter').lower():
            current_film = film
    
    
    print(current_film.find_next_sibling())    
    
    
if __name__ == '__main__':
    main()