import telebot
from config import keys, TOKEN
from extensions import GetWeatherException, WeatherCityBelarus

bot = telebot.TeleBot(TOKEN)

#обрабатываем команды start и help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<город Беларуси>\
\nПосмотреть список всех доступных городов: /values'
    bot.reply_to(message, text)    

    
#обрабатываем команду values
@bot.message_handler(commands=['values'])
def send_welcome(message: telebot.types.Message):
    text = 'Доступные города Беларуси:'
    for key in keys.keys(): # выводим все города из словаря
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#основная функция обработки текстовых запросов
@bot.message_handler(content_types=['text', ])
def get_weather(message: telebot.types.Message):
    try:  
        values = message.text.split(' ')
        if len(values) != 1:
            raise GetWeatherException('Слишком много параметров ввели.')
        text = WeatherCityBelarus.get_weather(values[0]) #вызываем метод класса, передав введеный текст пользователя
    except GetWeatherException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: \n{e}')
    else:
        bot.send_message(message.chat.id, text)

#если пользователь ввел не текст, то выводим ошибку
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def error_input(message: telebot.types.Message):
    bot.reply_to(message, f'Ошибка пользователя: \nВвели не текст! ')
    

bot.polling(none_stop=True)
    
    

