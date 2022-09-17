import requests
import json
from config import keys

class GetWeatherException(Exception):
    pass

class WeatherCityBelarus:
    @staticmethod
    def get_weather(city: str):
        try:
            coordinates_city = keys[city]
        except KeyError:
            raise GetWeatherException(f'Не удалось обработать город "{city}" \nПосмотреть список всех доступных городов: /values')
        #через API получаем данный с сайта open-meteo.com отправляя географическую широту и долготу города
        r = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coordinates_city[0]}&longitude={coordinates_city[1]}&current_weather=TRUE')
        #достаем текущую погоду из полученых данных
        current_weather = json.loads(r.content)['current_weather']
        temperature = current_weather['temperature']    #достаем температуру
        windspeed = current_weather['windspeed']        #достаем скорость ветра       
        return f' Погода в городе {city}:\nТемпература воздуха: {temperature}°C\nСкорость ветра: {windspeed} м/с'
    


