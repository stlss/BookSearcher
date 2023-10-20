import myfunction
import telebot
from telebot import types

token = '6646648697:AAHESBBAUnsZEGWFzvU6KykEX1IRXlJUtR0'
bot = telebot.TeleBot(token)
nameGenre_ = None  # С помощью этой переменной будем помнить, какой жанр пользователь выбирал.


# Обработка команды start.
@bot.message_handler(commands=['start'])
def show_greeting(message):
    # Создаём клавиатуру с одной кнопкой "Выбрать жанр".
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text='Выбрать жанр')
    keyboard.add(button)

    # Отправляем сообщение в чат, откуда пришёл {message}, передаём сообщение с приветствием и клавиатуру.
    bot.send_message(message.chat.id, myfunction.get_message_greeting(), reply_markup=keyboard)


# Обработка текстовых сообщений.
@bot.message_handler(content_types=['text'])
def hand_text(message):
    show_genres(message)
    show_sub_genres(message)
    show_books(message)


def show_genres(message):
    text = message.text

    # Если пользователь отправил сообщение "Выбрать жанр" или "Вернуться к выбору жанра", то показываем ему жанры.
    if text == 'Выбрать жанр' or text == 'Вернуться к выбору жанра':
        # Cоздаём клавиатуру с кнопками названиями жанров.
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        namesGenres = myfunction.get_names_genres()

        for nameGenre in namesGenres:
            button = types.KeyboardButton(text=nameGenre)
            keyboard.add(button)

        # Отправляем сообщение в чат, откуда пришёл {message}, передаём сообщение со списком жанров и клавиатуру.
        bot.send_message(message.chat.id, myfunction.get_message_names_genres(), reply_markup=keyboard)


def show_sub_genres(message):
    global nameGenre_

    nameGenre = message.text

    # Если пользователь ранее не выбирал жанр и отправленный жанр существует, то показываем ему поджанры.
    if nameGenre_ is None and myfunction.is_genre(nameGenre):
        # Запоминаем выбранный жанр.
        nameGenre_ = nameGenre

        # Создаём клавиатуру с кнопкой "Вернуться к выбору жанра" и кнопками с названиями поджанров.
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        button = types.KeyboardButton(text='Вернуться к выбору жанра')
        keyboard.add(button)

        namesSubGenres = myfunction.get_names_sub_genres(nameGenre)

        for nameSubGenre in namesSubGenres:
            button = types.KeyboardButton(text=nameSubGenre)
            keyboard.add(button)

        # Отправляем сообщение в чат, откуда пришёл {message}, передаём сообщение со списком поджанров и клавиатуру.
        bot.send_message(message.chat.id, myfunction.get_message_names_sub_genres(nameGenre), reply_markup=keyboard)


def show_books(message):
    nameSubGenre = message.text

    # Если отправленный поджанр существует, то покажем пользователю список книг.
    if myfunction.is_sub_genre(nameGenre_, nameSubGenre):
        bot.send_message(message.chat.id, "Топ 3 книги на сайте Литмир'а:\n")

        messages = myfunction.get_messages_books(nameGenre_, nameSubGenre)
        refs = myfunction.get_refs_books(nameGenre_, nameSubGenre)

        # zip - для одновременного перебора элементов из нескольких списков
        # Более подробно про zip https://pythoner.name/zip.
        for message_, ref in zip(messages, refs):
            # Создаём клавиатура (которая будет в сообщение с информацией о книге) с одной кнопкой.
            # По нажатию кнопки, будет открываться ссылка на книгу.
            keyboard = types.InlineKeyboardMarkup()
            urlButton = types.InlineKeyboardButton(text='Полное описание', url=ref)
            keyboard.add(urlButton)

            # Отправляем сообщение в чат, откуда пришёл {message}, передаём сообщение с инфой о книге и клавиатуру.
            bot.send_message(message.chat.id, message_, reply_markup=keyboard)


if __name__ == '__main__':
    bot.infinity_polling()
