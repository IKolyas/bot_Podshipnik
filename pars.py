import requests
from bs4 import BeautifulSoup as BS


"""Информация о погоде в определённом городе по запросу"""

opWM = os.environ.get('OpenWeatherMap')
class Weather:

    apiID = opWM

    def __init__(self, city):
        self.city = city
        self.wind = ''

    def reqGet(self):
        # Запрос на наличие города в базе данных OpenWeatherMap и получение ID города
        s_city = f"{self.city}, RU"
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': self.apiID})
            data = res.json()
            city_id = data['list'][0]['id']
            return city_id
        except Exception as e:
            print("Ошибка данных: ", e)
            pass

    def weather_in_day(self):
        # Получение информации о текущей погоде на сутки
        city_ID = self.reqGet()
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_ID, 'units': 'metric', 'lang': 'ru', 'APPID': self.apiID})
        data = res.json()
        degWind = data['wind']['deg']
        if 22 <= degWind < 67:  # Определяем направление ветра
            self.wind = "Северо-Восток"
        elif 67 <= degWind < 112:
            self.wind = "Восток"
        elif 112 <= degWind < 157:
            self.wind = "Юго-Восток"
        elif 157 <= degWind < 202:
            self.wind = "Юг"
        elif 202 <= degWind < 247:
            self.wind = "Юго-Запад"
        elif 247 <= degWind < 292:
            self.wind = "Запад"
        elif 292 <= degWind < 337:
            self.wind = "Северо-Запад"
        else:
            self.wind = "Северо-Запад"
        return f"Погода в городе {self.city}: \n" \
               f"Температура воздуха: {data['main']['temp']}°С " \
               f"({data['main']['temp_min']}...{data['main']['temp_max']}°С)\n" \
               f"    ощущается как {data['main']['feels_like']}°С, {data['weather'][0]['description']} \n" \
               f"Ветер: {data['wind']['speed']} м/с, \n" \
               f"    направление: {data['wind']['deg']}°, {self.wind}"

    def weather_in_5Day(self):
        # Получение информации о текущей погоде на 5 дней/в работе
        cityID = self.reqGet()
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'id': cityID, 'units': 'metric', 'lang': 'ru', 'APPID': self.apiID})
            data = res.json()
            print(data['list'])
            for i in data['list']:
                print(i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'])

        except Exception as e:
            print("Exception (forecast):", e)
            pass


# Парсинг инфа о вирусе
def pars_virus(city='Салехард'):
    kr_virus = requests.get(f'https://koronainfo.ru/{city}')
    virus_html = BS(kr_virus.content, 'html.parser')
    for _ in virus_html.select('.statistic-block-item'):
        active_all = virus_html.select('.active .total')[0].text
        active_today = virus_html.select('.active .bold')[0].text
        print(_)
    for _ in virus_html.select('.statistic-block-item'):
        recovered_all = virus_html.select('.recovered .total')[0].text
        recovered_today = virus_html.select('.recovered .bold')[0].text
        print(_)
    return f'''На данный период времени в городе {city}: \n
           Заражено: {active_all} чел. {active_today} (сегодня) \n
           Выздоровело: {recovered_all} чел. {recovered_today} (сегодня) \n
           '''


def parser_news():
    viki = requests.get(f'https://ria.ru/')
    html_viki = BS(viki.content, 'html.parser')

    for _ in html_viki.select(' .cell'):
        try:
            news = html_viki.select('.cell-list__item .cell-list__item-title')[0].text
            news1 = html_viki.select('.cell-list__item .cell-list__item-title')[1].text
            news2 = html_viki.select('.cell-list__item .cell-list__item-title')[2].text
            news3 = html_viki.select('.cell-list__item .cell-list__item-title')[3].text
            return f'Новости ... \n- {news} \n- {news1} \n- {news2} \n- {news3} \nБольше новостей и подробности на портале ...'
        except Exception:
            pass
