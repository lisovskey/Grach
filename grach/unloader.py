from datetime import datetime, timedelta
from urllib.request import urlopen
from requests import get
from requests.exceptions import ConnectionError
import json
import bs4


SHEDULE_URL = '  https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup='
FILMS_URL = 'http://afisha.360.by/category-films_schedule.html'
CRYPTORATE_URL = 'https://api.coinmarketcap.com/v1/ticker/'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?id=625144&units=metric&lang=ru&appid=75c166eea6260f05d427e10e67c89d94'


def get_schedule(group, delta):
    """
    return schedule from bsuir.by with delta days
    """
    week_days = ['в понедельник', 'во вторник', 'в среду', 'в четверг',
                 'в пятницу', 'в субботу', 'в воскресенье']

    try:
        full_schedule = json.load(urlopen(SHEDULE_URL + group))
    except ConnectionError:
        return None

    request_date = datetime.today() + timedelta(days=delta)
    day_num = request_date.timetuple()[6]
    week_num = full_schedule['currentWeekNumber']
    schedule = '{} {}'.format(group, week_days[day_num])
    try:
        subject = full_schedule['schedules'][day_num]
        schedule += ':'
    except IndexError:
        return schedule + ' отдыхает'

    for subject in subject['schedule']:
        if week_num in subject['weekNumber']:
            schedule += '\n\n{}'.format(subject['lessonTime'])
            if subject['numSubgroup'] != 0:
                schedule += ' ({} подгруппа)'.format(str(subject['numSubgroup']))
            schedule += '\n{} ({}) '.format(subject['subject'],
                                            subject['lessonType'])
            if subject['auditory']:
                schedule += subject['auditory'][0]
            if subject['employee'] and subject['numSubgroup'] == 0:
                schedule += ' {}'.format(subject['employee'][0]['lastName'])

    return schedule


def get_films(delta):
    """
    return list of films from 360.by
    """
    premieres = ''

    date = datetime.now() + timedelta(days=delta, hours=3)
    date = date.strftime('%d.%m.%Y')
    try:
        resp = get(FILMS_URL)
        soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    except (ConnectionError, bs4.FeatureNotFound):
        return None

    sub_soup = soup.body.section.select('.items-block > .items-sub-block > .cinema_slider > ul')[0]
    films = sub_soup.find_all('li', class_='scene')

    for i, film in enumerate(films):
        film_title = film.select('.movie > .info > header > h1')[0]
        premieres += '{}. {}\n'.format(i + 1, film_title.string)

    return premieres


def get_cryptorate(currency_name):
    """
    return exchange rate if exists
    """
    try:
        currency = get(CRYPTORATE_URL + currency_name).json()[0]
        return str(round(float(currency['price_usd']), 2))
    except KeyError:
        return None


def get_weather():
    """
    return current weather in minsk
    """
    data = get(WEATHER_URL).json()
    try:
        weather = ''
        for parameter in data['weather']:
            weather += '{}, '.format(parameter['description'])
        weather = weather.capitalize()
        weather += '{} °C\n'.format(data['main']['temp'])
        weather += 'Влажность {}%\n'.format(data['main']['humidity'])
        weather += 'Ветер {} м/с'.format(data['wind']['speed'])
        return weather
    except KeyError:
        return None
