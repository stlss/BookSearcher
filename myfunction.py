import myparser

dictionaryGenres = myparser.get_dictionary_genres()


# Получить названия всех жанров в алфавитном порядке.
def get_names_genres():
    namesGenres = list(dictionaryGenres.keys())
    namesGenres.sort()
    return namesGenres


# Получить названия всех поджанров в алфавитном порядке жанра {nameGenre}.
def get_names_sub_genres(nameGenre):
    namesSubGenres = list(dictionaryGenres[nameGenre].keys())
    namesSubGenres.sort()
    return namesSubGenres


# Проверка, что строка {genre} является жанром.
def is_genre(genre):
    return genre in dictionaryGenres


# Проверка, что строка {subGenre} является поджанром жанра {subGenre}.
def is_sub_genre(genre, subGenre):
    return genre in dictionaryGenres and subGenre in dictionaryGenres[genre]


# Получить сообщение с приветствием.
def get_message_greeting():
    return 'Привет! Это бот по поиску книг.\nВыбрав жанр и поджанр, вы получите подборку книг.'


# Получить сообщение с нумерованным списком названий жанров.
def get_message_names_genres():
    namesGenres = get_names_genres()

    for i in range(len(namesGenres)):
        namesGenres[i] = str(i + 1) + ') ' + namesGenres[i]

    return 'Список жанров:\n' + '\n'.join(namesGenres)


# Получить сообщение с нумерованным списком названий поджанров жанра {nameGenre}.
def get_message_names_sub_genres(nameGenre):
    namesSubGenres = get_names_sub_genres(nameGenre)

    for i in range(len(namesSubGenres)):
        namesSubGenres[i] = str(i + 1) + ') ' + namesSubGenres[i]

    return f'Список поджанров ({nameGenre}):\n' + '\n'.join(namesSubGenres)


# Получить список сообщений с информацией о книгах жанра {nameGenre} поджанра {nameSubGenre}.
def get_messages_books(nameGenre, nameSubGenre):
    dictionaryBooks = myparser.get_dictionary_books(dictionaryGenres, nameGenre, nameSubGenre)
    messages = list()

    for key, value in dictionaryBooks.items():
        message = f'"{key}"' + '\n\n' + \
                  'Автор: ' + ' '.join(value['authors']) + '\n\n' \
                  + f'Оценка: {value["grade"]}' + '\n\n' + value['description']
        messages.append(message)

    return messages


# Получить список ссылок на книги жанра {nameGenre} поджанра {nameSubGenre}.
def get_refs_books(nameGenre, nameSubGenre):
    dictionaryBooks = myparser.get_dictionary_books(dictionaryGenres, nameGenre, nameSubGenre)
    refs = list()

    for value in dictionaryBooks.values():
        ref = value['ref']
        refs.append(ref)

    return refs
