import telebot
from binance_api import Binance
from tg_api import bot_key
from telebot import types
from cbr_rates import dollar_cbr
from cbr_rates import euro_cbr

token = bot_key()
bot = telebot.TeleBot(token)


crypto_bot = Binance(
API_KEY='Your_Key',
API_SECRET='Your_Key'
)

p_btc = crypto_bot.tickerPrice(symbol='BTCUSDT')
price_btc = p_btc['price']

p_eth = crypto_bot.tickerPrice(symbol='ETHUSDT')
price_eth = p_eth['price']

p_trx = crypto_bot.tickerPrice(symbol='TRXUSDT')
price_trx = p_trx['price']

p_bnb = crypto_bot.tickerPrice(symbol='BNBUSDT')
price_bnb = p_bnb['price']

p_eos = crypto_bot.tickerPrice(symbol='EOSUSDT')
price_eos = p_eos['price']

p_xrp = crypto_bot.tickerPrice(symbol='XRPUSDT')
price_xrp = p_xrp['price']

p_usd = dollar_cbr()
p_euro = euro_cbr()

currencies = ['btc', 'eth', 'trx', 'bnb', 'eos', 'xrp', 'usd', 'euro']


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text=c, callback_data=c) for c in currencies]
    keyboard.add(*buttons)
    return keyboard


@bot.callback_query_handler(func=lambda x: True)
def callback_handler(callback_query):
    message = callback_query.message
    text = callback_query.data
    currency, value = check_currency_value(text)
    if currency:
        bot.send_message(chat_id=message.chat.id, text='Курс {} равен {}'.format(currency, value))


def check_currency(message):
    for c in currencies:
        if c in message.text.lower():
            return True
    return False


def check_currency_value(text):
    currency_values = {'btc': str(price_btc) + ' usdt', 'eth': str(price_eth) + ' usdt', 'trx': str(price_trx) +
                       ' usdt', 'bnb': str(price_bnb) + ' usdt', 'eos': str(price_eos) + ' usdt',
                       'xrp': str(price_xrp) + ' usdt', 'usd': str(p_usd) + ' rub', 'euro': str(p_euro) + ' rub'}
    for currency, value in currency_values.items():
        if currency in text.lower():
            return currency, value
    return None, None


@bot.message_handler(func=check_currency)
def handle_currency(message):
    currency, value = check_currency_value(message.text)
    keyboard = create_keyboard()
    if currency:
        bot.send_message(chat_id=message.chat.id, text='Курс {} равен {}'.format(currency, value),
                         reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text='Укажите нужную валюту',
                         reply_markup=keyboard)

@bot.message_handler()
def handle_message(message):
    keyboard = create_keyboard()
    bot.send_message(chat_id=message.chat.id, text='Узнай курс валют', reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
