import telebot
from config import token, keys
from extensions import APIException, Exchange


def telegram_bot(bot_token):

    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start'])
    def start(message: telebot.types.Message):
        text = 'Бот-Конвертер валют приветствует Вас!\n' \
               'Для конвертации валют, введите команду в следующем формате: \n' \
               '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
               'или\n' \
               '<количество переводимой валюты> <имя валюты> <в какую валюту перевести> \n' \
               'например: 100 рубль доллар   или   евро доллар 15\n' \
               '/values - Показывает список всех доступных валют\n' \
               '/help - Помощь по командам бота'
        bot.reply_to(message, text)

    @bot.message_handler(commands=['help'])
    def help_(message: telebot.types.Message):
        text = 'Для конвертации валют, введите команду в следующем формате: \n' \
               '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
               'или\n' \
               '<количество переводимой валюты> <имя валюты> <в какую валюту перевести>\n' \
               'например: 100 рубль доллар   или   евро доллар 15\n' \
               '/values - Показывает список всех доступных валют'
        bot.reply_to(message, text)

    @bot.message_handler(commands=['values'])
    def values_(message: telebot.types.Message):
        text = 'Доступные валюты для конвертации:'
        for key in keys.keys():
            text = '\n'.join((text, key))
        bot.reply_to(message, text)

    @bot.message_handler(content_types=['text'])
    def get_price(message: telebot.types.Message):
        try:
            values = message.text.lstrip().rstrip().split(' ')

            if len(values) != 3:
                raise APIException('Введите команду (/help) или три параметра для конвертации')
            if values[0].isdigit():
                amount, base, quote = values
            else:
                base, quote, amount = values
            total_quote = Exchange.get_price(base, quote, amount)
        except APIException as e:
            bot.reply_to(message, f'Ошибка пользователя.\n{e}')
        except Exception as e:
            bot.reply_to(message, f'Что-то пошло не так {e}')
        else:
            text = f'Переводим {base} в {quote}\n{amount} {base} = {total_quote:.2f} {quote}'
            bot.send_message(message.chat.id, text)

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
